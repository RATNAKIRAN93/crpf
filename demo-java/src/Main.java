import com.sun.net.httpserver.*; import java.io.*; import java.net.*;
public class Main {
  public static void main(String[] args) throws Exception {
    HttpServer s = HttpServer.create(new InetSocketAddress(8081), 0);
    s.createContext("/", ex -> { String r="OK\n"; try{Thread.sleep(50);}catch(Exception ignored){}
      ex.sendResponseHeaders(200, r.length());
      try(OutputStream os=ex.getResponseBody()) { os.write(r.getBytes()); }});
    s.setExecutor(null);
    System.out.println("Demo listening on http://localhost:8080");
    s.start();
  }
}
