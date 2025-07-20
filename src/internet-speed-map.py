import speedtest
import geocoder
import json
import os
from datetime import datetime

def run_speedtest():
    
    st = speedtest.Speedtest()
    
    
    st.get_best_server()  
    
    # Medições
    download = st.download() / 1e6  
    upload = st.upload() / 1e6
    ping = st.results.ping
    
    
    g = geocoder.ip('me')
    
    
    return {
        "timestamp": str(datetime.now()),
        "download_mbps": round(download, 2),
        "upload_mbps": round(upload, 2),
        "ping_ms": round(ping, 2),
        "location": {
            "latitude": g.latlng[0] if g.latlng else None,
            "longitude": g.latlng[1] if g.latlng else None,
            "city": g.city,
            "isp": st.results.client.get("isp", "Desconhecido")
        },
        "server": {
            "name": st.results.server.get("name", "Desconhecido"),
            "distance_km": round(st.results.server.get("d", 0), 2)
        }
    }


os.makedirs("data", exist_ok=True)


data = run_speedtest()
filename = f"data/speedtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"✅ Teste concluído! Dados salvos em {filename}")