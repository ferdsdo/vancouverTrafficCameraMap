import requests
from bs4 import BeautifulSoup
import json

# List of URLs to scrape
urls = [
'https://trafficcams.vancouver.ca/alma10.htm',
'https://trafficcams.vancouver.ca/anderson04.htm',
'https://trafficcams.vancouver.ca/andersonLameysMill.htm',
'https://trafficcams.vancouver.ca/angusMarine.htm',
'https://trafficcams.vancouver.ca/arbutus12.htm',
'https://trafficcams.vancouver.ca/arbutus16.htm',
'https://trafficcams.vancouver.ca/arbutusBroadway.htm',
'https://trafficcams.vancouver.ca/arbutusGreenwaySWMarine.htm',
'https://trafficcams.vancouver.ca/arbutusLahb.htm',
'https://trafficcams.vancouver.ca/arbutusWKingEdward.htm',
'https://trafficcams.vancouver.ca/argylemarine.htm',
'https://trafficcams.vancouver.ca/ash10.htm',
'https://trafficcams.vancouver.ca/BeattyDunsmuir.htm',
'https://trafficcams.vancouver.ca/beattyGeorgia.htm',
'https://trafficcams.vancouver.ca/beattySmithe.htm',
'https://trafficcams.vancouver.ca/blanca10.htm',
'https://trafficcams.vancouver.ca/boulevards41.htm',
'https://trafficcams.vancouver.ca/boundary1.htm',
'https://trafficcams.vancouver.ca/boundary22.htm',
'https://trafficcams.vancouver.ca/boundary29.htm',
'https://trafficcams.vancouver.ca/boundary49.htm',
'https://trafficcams.vancouver.ca/boundaryCanadaWay.htm',
'https://trafficcams.vancouver.ca/BoundaryGrandviewHwy.htm',
'https://trafficcams.vancouver.ca/boundaryHenning.htm',
'https://trafficcams.vancouver.ca/boundaryKingsway.htm',
'https://trafficcams.vancouver.ca/boundaryLougheed.htm',
'https://trafficcams.vancouver.ca/boundaryVanness.htm',
'https://trafficcams.vancouver.ca/broadwayGranville.htm',
'https://trafficcams.vancouver.ca/burrard12.htm',
'https://trafficcams.vancouver.ca/burrard4.htm',
'https://trafficcams.vancouver.ca/BurrardBridge.htm',
'https://trafficcams.vancouver.ca/BurrardCanadaPlace.htm',
'https://trafficcams.vancouver.ca/BurrardCornwall4.htm',
'https://trafficcams.vancouver.ca/burrardDavie.htm',
'https://trafficcams.vancouver.ca/burrardDrake.htm',
'https://trafficcams.vancouver.ca/burrardnelson.htm',
'https://trafficcams.vancouver.ca/BurrardPacific4.htm',
'https://trafficcams.vancouver.ca/burrardSmithe.htm',
'https://trafficcams.vancouver.ca/buteDavie.htm',
'https://trafficcams.vancouver.ca/cambie12.htm',
'https://trafficcams.vancouver.ca/cambie16th.htm',
'https://trafficcams.vancouver.ca/cambie25.htm',
'https://trafficcams.vancouver.ca/cambie29.htm',
'https://trafficcams.vancouver.ca/cambie2East.htm',
'https://trafficcams.vancouver.ca/cambie2West.htm',
'https://trafficcams.vancouver.ca/cambie33.htm',
'https://trafficcams.vancouver.ca/cambie37.htm',
'https://trafficcams.vancouver.ca/cambie41.htm',
'https://trafficcams.vancouver.ca/cambie49.htm',
'https://trafficcams.vancouver.ca/cambiebridge.htm',
'https://trafficcams.vancouver.ca/cambieBroadway.htm',
'https://trafficcams.vancouver.ca/CambieMarine.htm',
'https://trafficcams.vancouver.ca/cambieNelson.htm',
'https://trafficcams.vancouver.ca/campbellHastings.htm',
'https://trafficcams.vancouver.ca/carnarvon41.htm',
'https://trafficcams.vancouver.ca/carolinaGreatNorthern.htm',
'https://trafficcams.vancouver.ca/cassiarHastings.htm',
'https://trafficcams.vancouver.ca/clark12.htm',
'https://trafficcams.vancouver.ca/clark4.htm',
'https://trafficcams.vancouver.ca/clarkBroadway.htm',
'https://trafficcams.vancouver.ca/ClarkHastings.htm',
'https://trafficcams.vancouver.ca/ClarkPowell.htm',
'https://trafficcams.vancouver.ca/collectorsBridgeway.htm',
'https://trafficcams.vancouver.ca/Commercial01.htm',
'https://trafficcams.vancouver.ca/commercialBroadway.htm',
'https://trafficcams.vancouver.ca/cornishSWMarine.htm',
'https://trafficcams.vancouver.ca/denman3.htm',
'https://trafficcams.vancouver.ca/denmanBeach.htm',
'https://trafficcams.vancouver.ca/denmanDavie.htm',
'https://trafficcams.vancouver.ca/dunbar41.htm',
'https://trafficcams.vancouver.ca/EarlesKingsway.htm',
'https://trafficcams.vancouver.ca/expoSmithe.htm',
'https://trafficcams.vancouver.ca/frasermarine.htm',
'https://trafficcams.vancouver.ca/georgia3.htm',
'https://trafficcams.vancouver.ca/gladstoneKingsway.htm',
'https://trafficcams.vancouver.ca/glenPowell.htm',
'https://trafficcams.vancouver.ca/grandview4.htm',
'https://trafficcams.vancouver.ca/granville12.htm',
'https://trafficcams.vancouver.ca/granville16.htm',
'https://trafficcams.vancouver.ca/granville41.htm',
'https://trafficcams.vancouver.ca/granville70th.htm',
'https://trafficcams.vancouver.ca/GranvilleDunsmuir.htm',
'https://trafficcams.vancouver.ca/granvilleGeorgia.htm',
'https://trafficcams.vancouver.ca/granvillehastings.htm',
'https://trafficcams.vancouver.ca/granvilleNelson.htm',
'https://trafficcams.vancouver.ca/granvillerobson.htm',
'https://trafficcams.vancouver.ca/granvilleSmithe.htm',
'https://trafficcams.vancouver.ca/greenway12.htm',
'https://trafficcams.vancouver.ca/hastings.htm',
'https://trafficcams.vancouver.ca/hornbyDrake.htm',
'https://trafficcams.vancouver.ca/hornbyGeorgia.htm',
'https://trafficcams.vancouver.ca/hornbyNelson.htm',
'https://trafficcams.vancouver.ca/hornbyPacific.htm',
'https://trafficcams.vancouver.ca/HornbyRobson.htm',
'https://trafficcams.vancouver.ca/hornbySmithe.htm',
'https://trafficcams.vancouver.ca/howeDrake.htm',
'https://trafficcams.vancouver.ca/howeGeorgia.htm',
'https://trafficcams.vancouver.ca/howePacific.htm',
'https://trafficcams.vancouver.ca/joyceKingsway.htm',
'https://trafficcams.vancouver.ca/joyceVanness.htm',
'https://trafficcams.vancouver.ca/kerr54.htm',
'https://trafficcams.vancouver.ca/kerrMarine.htm',
'https://trafficcams.vancouver.ca/kingsway10.htm',
'https://trafficcams.vancouver.ca/kingsway11.htm',
'https://trafficcams.vancouver.ca/kingswayBroadway.htm',
'https://trafficcams.vancouver.ca/kinrossMarine.htm',
'https://trafficcams.vancouver.ca/knight.htm',
'https://trafficcams.vancouver.ca/knight49.htm',
'https://trafficcams.vancouver.ca/knight57.htm',
'https://trafficcams.vancouver.ca/knightKingEdward.htm',
'https://trafficcams.vancouver.ca/knightKingsway.htm',
'https://trafficcams.vancouver.ca/knightMarineBridge.htm',
'https://trafficcams.vancouver.ca/macdonald16.htm',
'https://trafficcams.vancouver.ca/macdonald4.htm',
'https://trafficcams.vancouver.ca/macdonald8.htm',
'https://trafficcams.vancouver.ca/macdonaldBroadway.htm',
'https://trafficcams.vancouver.ca/macdonaldKitsDiv.htm',
'https://trafficcams.vancouver.ca/Main2.htm',
'https://trafficcams.vancouver.ca/main33.htm',
'https://trafficcams.vancouver.ca/mainBroadway.htm',
'https://trafficcams.vancouver.ca/MainHastings.htm',
'https://trafficcams.vancouver.ca/mainKingsway7.htm',
'https://trafficcams.vancouver.ca/mainmarine.htm',
'https://trafficcams.vancouver.ca/mainTerminal.htm',
'https://trafficcams.vancouver.ca/manitoba2.htm',
'https://trafficcams.vancouver.ca/manitobamarine.htm',
'https://trafficcams.vancouver.ca/maple41.htm',
'https://trafficcams.vancouver.ca/marine41.htm',
'https://trafficcams.vancouver.ca/marine49.htm',
'https://trafficcams.vancouver.ca/marine70.htm',
'https://trafficcams.vancouver.ca/marineMarineWay.htm',
'https://trafficcams.vancouver.ca/mcleanPowell.htm',
'https://trafficcams.vancouver.ca/nanaimo1.htm',
'https://trafficcams.vancouver.ca/nanaimo24.htm',
'https://trafficcams.vancouver.ca/nanaimobroadway.htm',
'https://trafficcams.vancouver.ca/nanaimoDundas.htm',
'https://trafficcams.vancouver.ca/nanaimoGrandview.htm',
'https://trafficcams.vancouver.ca/nanaimoHastings.htm',
'https://trafficcams.vancouver.ca/oak12.htm',
'https://trafficcams.vancouver.ca/oak33.htm',
'https://trafficcams.vancouver.ca/oak4.htm',
'https://trafficcams.vancouver.ca/oak49.htm',
'https://trafficcams.vancouver.ca/oakW10.htm',
'https://trafficcams.vancouver.ca/oakWBroadway.htm',
'https://trafficcams.vancouver.ca/pine12.htm',
'https://trafficcams.vancouver.ca/quebec2.htm',
'https://trafficcams.vancouver.ca/quebecSwitchmen.htm',
'https://trafficcams.vancouver.ca/raymurVenables.htm',
'https://trafficcams.vancouver.ca/renfrew01st.htm',
'https://trafficcams.vancouver.ca/renfrew22.htm',
'https://trafficcams.vancouver.ca/renfrewAdanac.htm',
'https://trafficcams.vancouver.ca/renfrewBroadway.htm',
'https://trafficcams.vancouver.ca/renfrewGrandview.htm',
'https://trafficcams.vancouver.ca/renfrewHastings.htm',
'https://trafficcams.vancouver.ca/renfrewPandora.htm',
'https://trafficcams.vancouver.ca/richardsCordovaWater.htm',
'https://trafficcams.vancouver.ca/richardsDavie.htm',
'https://trafficcams.vancouver.ca/richardsDrake.htm',
'https://trafficcams.vancouver.ca/richardsDunsmuir.htm',
'https://trafficcams.vancouver.ca/richardsGeorgia.htm',
'https://trafficcams.vancouver.ca/richardsHastings.htm',
'https://trafficcams.vancouver.ca/richardsHelmcken.htm',
'https://trafficcams.vancouver.ca/richardsNelson.htm',
'https://trafficcams.vancouver.ca/richardsPacific.htm',
'https://trafficcams.vancouver.ca/richardsPender.htm',
'https://trafficcams.vancouver.ca/richardsRobson.htm',
'https://trafficcams.vancouver.ca/richardsSmithe.htm',
'https://trafficcams.vancouver.ca/RiverDistrictMarine.htm',
'https://trafficcams.vancouver.ca/ross41.htm',
'https://trafficcams.vancouver.ca/rupert03rd.htm',
'https://trafficcams.vancouver.ca/rupert41.htm',
'https://trafficcams.vancouver.ca/rupert45.htm',
'https://trafficcams.vancouver.ca/rupertE22.htm',
'https://trafficcams.vancouver.ca/sasamat10.htm',
'https://trafficcams.vancouver.ca/SawmillEastMarine.htm',
'https://trafficcams.vancouver.ca/SawmillWestMarine.htm',
'https://trafficcams.vancouver.ca/scotia2.htm',
'https://trafficcams.vancouver.ca/seymourDunsmuir.htm',
'https://trafficcams.vancouver.ca/seymourGeorgia.htm',
'https://trafficcams.vancouver.ca/seymourNelson.htm',
'https://trafficcams.vancouver.ca/seymourRobson.htm',
'https://trafficcams.vancouver.ca/seymourSmithe.htm',
'https://trafficcams.vancouver.ca/slocanKingsway.htm',
'https://trafficcams.vancouver.ca/ThurlowCanadaPlace.htm',
'https://trafficcams.vancouver.ca/thurlowPacific.htm',
'https://trafficcams.vancouver.ca/victoria12.htm',
'https://trafficcams.vancouver.ca/victoria41.htm',
'https://trafficcams.vancouver.ca/victoria49.htm',
'https://trafficcams.vancouver.ca/victoriaMarine.htm',
'https://trafficcams.vancouver.ca/victoriaVictoriaCommercial.htm',
'https://trafficcams.vancouver.ca/yukonSWMarine.htm'
]

# Function to scrape a URL and extract the desired HTML content
def scrape_url(url):
    try:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the section with the class 'section--container'
        section_container = soup.find('div', class_='section--container')

        # If the section container is found, look for all 'camera' divs inside it
        if section_container:
            camera_divs = section_container.find_all('div', class_='camera')

            # Return the list of camera divs (raw HTML or text)
            return [str(camera) for camera in camera_divs]
        else:
            return None  # If no section container is found

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

# Dictionary to store the scraped HTML content for each URL
scraped_data = {}

# Loop through the URLs and scrape each one
for url in urls:
    print(f"Scraping {url}...")
    html_content = scrape_url(url)
    
    if html_content:
        scraped_data[url] = html_content
    else:
        scraped_data[url] = []  # Store an empty list if no relevant content found

# Output the results to a JSON file
output_filename = 'scraped_data.json'
with open(output_filename, 'w') as json_file:
    json.dump(scraped_data, json_file, indent=4)

print(f"Scraping complete. Results saved to {output_filename}.")
