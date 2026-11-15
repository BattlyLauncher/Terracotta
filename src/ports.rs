use std::io;
use std::net::{Ipv4Addr, TcpListener, UdpSocket};

#[repr(u8)]
pub enum PortRequest {
    #[allow(dead_code)]
    EasyTierRPC,
    Scaffolding,
    Minecraft
}

impl PortRequest {
    pub fn request_specific(port: u16) -> io::Result<u16> {
        // EasyTier binds the wildcard address for both TCP and UDP. A loopback-only
        // probe can succeed on Windows while that wildcard port is already in use.
        let tcp = TcpListener::bind((Ipv4Addr::UNSPECIFIED, port))?;
        let selected = tcp.local_addr()?.port();
        let _udp = UdpSocket::bind((Ipv4Addr::UNSPECIFIED, selected))?;
        Ok(selected)
    }

    pub fn request(self) -> u16 {
        TcpListener::bind((Ipv4Addr::LOCALHOST, 0))
            .and_then(|socket| socket.local_addr())
            .map(|address| address.port())
            .unwrap_or(self as u8 as u16 + 35780)
    }
}
#[cfg(test)]
mod tests {
 use super::*;
 #[test] fn rejects_udp_port_already_in_use() {
  let udp=UdpSocket::bind((Ipv4Addr::UNSPECIFIED,0)).unwrap();
  assert!(PortRequest::request_specific(udp.local_addr().unwrap().port()).is_err());
 }
 #[test] fn accepts_unused_tcp_and_udp_port() {
  assert!(PortRequest::request_specific(0).unwrap()>0);
 }
}
