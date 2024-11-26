import argparse
import geoip2.database
from geoip2.errors import AddressNotFoundError
import ipaddress

def get_ip_geolocation(ip_address: str) -> dict:
    """
    Get geolocation data for an IP address using local MaxMind GeoLite2 databases
    """
    # Validate IP address format
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        raise ValueError(f"Invalid IP address format: {ip_address}")
        
    result = {
        'country_name': 'Unknown',
        'country_code': 'Unknown',
        'city': 'Unknown',
        'latitude': 'Unknown',
        'longitude': 'Unknown',
        'isp': 'Unknown'
    }
    
    # Separate try blocks for better error handling
    try:
        with geoip2.database.Reader('databases/GeoLite2-City.mmdb') as city_reader:
            city_response = city_reader.city(ip_address)
            result.update({
                'country_name': city_response.country.name or 'Unknown',  # Handle None values
                'country_code': city_response.country.iso_code or 'Unknown',
                'city': city_response.city.name or 'Unknown',
                'latitude': city_response.location.latitude or 'Unknown',
                'longitude': city_response.location.longitude or 'Unknown'
            })
    except FileNotFoundError:
        print("[!] Error: GeoLite2-City database file not found. Please download it from MaxMind.")
    except AddressNotFoundError:
        print(f"[!] IP address {ip_address} not found in the City database")
    
    try:
        with geoip2.database.Reader('databases/GeoLite2-ASN.mmdb') as asn_reader:
            asn_response = asn_reader.asn(ip_address)
            result['isp'] = asn_response.autonomous_system_organization or 'Unknown'
    except FileNotFoundError:
        print("[!] Error: GeoLite2-ASN database file not found. Please download it from MaxMind.")
    except AddressNotFoundError:
        print(f"[!] IP address {ip_address} not found in the ASN database")
    
    return result

def display_geolocation_info(geo_data: dict) -> None:
    """Display formatted geolocation information"""
    print("\n[*] Geolocation Information:")
    print(f"    Country: {geo_data['country_name']} ({geo_data['country_code']})")
    print(f"    City: {geo_data['city']}")
    print(f"    Latitude: {geo_data['latitude']}")
    print(f"    Longitude: {geo_data['longitude']}")
    print(f"    ISP: {geo_data['isp']}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_address', required=True, help='IP Address to Check')
    args = parser.parse_args()
    
    try:
        print(f"\n[*] Checking IP: {args.ip_address}")
        
        # Get and display geolocation information
        geo_data = get_ip_geolocation(args.ip_address)
        display_geolocation_info(geo_data)
            
    except ValueError as e:
        print(f"[!] Invalid IP address format: {args.ip_address}")
        return

if __name__ == "__main__":
    main()
