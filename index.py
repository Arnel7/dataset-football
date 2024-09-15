
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

import pyfiglet

import json






import mysql.connector
retry = 0
max_retry = 8



def update_statistics_in_database(stats_data, idCoup):
   
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='football'
        )
        cursor = conn.cursor()

        for stats in stats_data:
    # Vérifier si stats est une liste de longueur 23
            if not isinstance(stats, (list, tuple)) or len(stats) != 23:
                print("Données de statistiques invalides:", stats)
                continue

    # Conversion des types si nécessaire
            stats_list = list(stats)
            print("liste est ",stats_list)

            match_id = stats_list[0]  # Extraire match_id
            stats_list[0] = int(match_id)  # match_id
            stats_list[3] = int(stats_list[3])  # team_a_shots_on_target
            stats_list[4] = int(stats_list[4])  # team_b_shots_on_target
          #  print("macth id  est ",match_id)

            for i in range(7, 21):  # Conversion des éléments de 7 à 20 en entiers
                stats_list[i] = int(stats_list[i])

            stats_list[21] = json.dumps(stats_list[21]) if isinstance(stats_list[21], list) else stats_list[21]  # Conversion en JSON si nécessaire
            stats_list[22] = json.dumps(stats_list[22]) if isinstance(stats_list[22], list) else stats_list[22]

    # Créer la liste des valeurs à mettre à jour
            update_values = ", ".join([f"{column} = %s" for column in [
                'match_id', 'team_a_short', 'team_b_short', 'team_a_shots_on_target', 'team_b_shots_on_target', 
                'team_a_possession', 'team_b_possession', 'team_a_passes', 'team_b_passes', 'team_a_pass_accuracy', 
                'team_b_pass_accuracy', 'team_a_fouls', 'team_b_fouls', 'team_a_yellow_cards', 'team_b_yellow_cards', 
                'team_a_red_cards', 'team_b_red_cards', 'team_a_offsides', 'team_b_offsides', 'team_a_corners', 
                'team_b_corners', 'team_a_goal_times', 'team_b_goal_times'
            ]])

            cursor.execute(f'''
    UPDATE euro
    SET 
    match_id = %s, 
    team_a_short = %s, 
    team_b_short = %s, 
    team_a_shots_on_target = %s, 
    team_b_shots_on_target = %s, 
    team_a_possession = %s, 
    team_b_possession = %s, 
    team_a_passes = %s, 
    team_b_passes = %s, 
    team_a_pass_accuracy = %s, 
    team_b_pass_accuracy = %s, 
    team_a_fouls = %s, 
    team_b_fouls = %s, 
    team_a_yellow_cards = %s, 
    team_b_yellow_cards = %s, 
    team_a_red_cards = %s, 
    team_b_red_cards = %s, 
    team_a_offsides = %s, 
    team_b_offsides = %s, 
    team_a_corners = %s, 
    team_b_corners = %s, 
    team_a_goal_times = %s, 
    team_b_goal_times = %s
    WHERE id = %s
''', stats_list + [match_id])

            

        conn.commit()
        print("Données de statistiques mises à jour dans la base de données.")

    except mysql.connector.Error as e:
        print("\033[91mErreur MySQL lors de la mise à jour des données de statistiques:", e, "\033[0m")

    finally:
        if conn:
            conn.close()



#update_statistics_in_database(stats_data, 1)  # Met à jour les statistiques pour l'idCoup 1



def savephp(data):
    # Connectez-vous à la base de données MySQL
    conn = mysql.connector.connect(
        host='localhost',  # Remplace par l'adresse de votre serveur MySQL
        user='root',  # Remplace par le nom d'utilisateur MySQL
        password='',  # Remplace par le mot de passe MySQL
        database='football'  # Remplacez par le nom de la base de données
    )
    cursor = conn.cursor()
    match_ids = []

    for match in data:
        cursor.execute('''
        INSERT INTO euro (date_text, unix_timestamp, team_a_logo_url, team_a_name, team_a_goal, team_b_logo_url, team_b_name, team_b_goal, day)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', match)
        conn.commit()
        match_id = cursor.lastrowid
        match_ids.append(match_id)

    conn.close()
    print("Data saved to database.")
    return match_ids


def format_date(date_text):
    """
    Converts a date string to the desired format.
    
    Args:
    date_text (str): The date string to be formatted.

    Returns:
    str: The formatted date string, or the original string if no formatting is needed.
    """
    try:
        # Try to parse the date string assuming it has a time component
        date_obj = datetime.strptime(date_text, '%d %b, %I:%M\u202f%p')
        # Format the datetime object to the desired format
        formatted_date = date_obj.strftime('%d %b, %I:%M %p')
    except ValueError:
        # If parsing fails, return the original date string
        formatted_date = date_text
    
    return formatted_date


def parse_date(date_str):
    formats_without_year = ["%a, %d %b", "%d %b, %I:%M %p"]
    formats_with_year = ["%d %b %y", "%a %d %b %y", "%d %b %y, %I:%M %p", "%a %d %b %y, %I:%M %p"]
    
    # Try formats without year first, assuming current year
    for fmt in formats_without_year:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            current_year = datetime.today().year
            return parsed_date.replace(year=current_year)
        except ValueError:
            continue
    
    # Try formats with year next
    for fmt in formats_with_year:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Date string {date_str} does not match any known format.")


def compare_with_today(date_str):
    try:
        date_obj = parse_date(date_str)
        date_only = date_obj.date()
        today_date = datetime.today().date()
        if today_date > date_only:
            return "past"
        else:
            return "future"
    except ValueError as e:
        return str(e)

def extract_info_from_html(soup, day,unix_timestamp):
    # soup = BeautifulSoup(html_content, 'html.parser')

    match_data = []
    stats_data = []
    date_text = ''
    team_a_logo_url = ''
    team_a_name = ''
    team_a_goal = ''
    team_b_logo_url = ''
    team_b_name = ''
    team_b_goal = ''

    try:
        # Extract date information
        imso_hide_overflow_div = soup.find('div', class_='imso-hide-overflow')
        spans = imso_hide_overflow_div.find_all('span')  # Only direct child span elements
        if len(spans) > 1:
            date = spans[4].text.strip()
            date_text = format_date(date)

    except Exception as e:
        print(f"An error occurred while extracting date: {e}")

    try:
        # Extract team A information
        team_a_logo_element = soup.select_one('.imso_mh__first-tn-ed .imso_btl__mh-logo')
        if team_a_logo_element:
            team_a_logo_url = team_a_logo_element['src']

        team_a_name_element = soup.select_one('.imso_mh__first-tn-ed .imso_mh__tm-nm .liveresults-sports-immersive__hide-element')
        if team_a_name_element:
            team_a_name = team_a_name_element.text
        team_a_goal_element = soup.select_one('.imso_mh__l-tm-sc')
        if team_a_goal_element:
            team_a_goal = team_a_goal_element.text
    except Exception as e:
        print(f"An error occurred while extracting team A information: {e}")

    try:
        # Extract team B information
        team_b_logo_element = soup.select_one('.imso_mh__second-tn-ed .imso_btl__mh-logo')
        if team_b_logo_element:
            team_b_logo_url = team_b_logo_element['src']
        team_b_name_element = soup.select_one('.imso_mh__second-tn-ed .imso_mh__tm-nm .liveresults-sports-immersive__hide-element')
        if team_b_name_element:
            team_b_name = team_b_name_element.text
        team_b_goal_element = soup.select_one('.imso_mh__r-tm-sc')
        if team_b_goal_element:
            team_b_goal = team_b_goal_element.text
    except Exception as e:
        print(f"An error occurred while extracting team B information: {e}")

    time.sleep(2)

    match_data.append([date_text, unix_timestamp, team_a_logo_url, team_a_name, team_a_goal, team_b_logo_url, team_b_name, team_b_goal, day])

    #match_id = save_data_to_database(match_data)
    match_id = savephp(match_data)

   # match
    date_res = compare_with_today(date_text)
   # if date_res == 'past':
    if 1 == 1:
        shots_rows = soup.find_all('tr', class_='MzWkAb')
        if shots_rows:
            shots_data = []
            for row in shots_rows:
                tds = row.find_all('td')
                for td in tds:
                    shots_data.append(td.text.strip())
            team_a_short = shots_data[0]
            team_b_short = shots_data[1]
            team_a_shots_on_target = shots_data[2]
            team_b_shots_on_target = shots_data[3]
            team_a_possession = shots_data[4].strip("%")
            team_b_possession = shots_data[5].strip("%")
            team_a_passes = shots_data[6]
            team_b_passes = shots_data[7]
            team_a_pass_accuracy = shots_data[8].strip("%")
            team_b_pass_accuracy = shots_data[9].strip("%")
            team_a_fouls = shots_data[10]
            team_b_fouls = shots_data[11]
            team_a_yellow_cards = shots_data[12]
            team_b_yellow_cards = shots_data[13]
            team_a_red_cards = shots_data[14]
            team_b_red_cards = shots_data[15]
            team_a_offsides = shots_data[16]
            team_b_offsides = shots_data[17]
            team_a_corners = shots_data[18]
            team_b_corners = shots_data[19]

            # Extract goal times
            team_a_goal_times = [span.text for span in soup.select('.imso_gs__left-team .liveresults-sports-immersive__game-minute span') if span.text.isdigit()]
            team_b_goal_times = [span.text for span in soup.select('.imso_gs__right-team .liveresults-sports-immersive__game-minute span') if span.text.isdigit()]
            
        
        team_a_goal_times_str = json.dumps(team_a_goal_times)
        team_b_goal_times_str = json.dumps(team_b_goal_times)

        stats_data.append([match_id[0], team_a_short, team_b_short, team_a_shots_on_target, team_b_shots_on_target, 
                    team_a_possession, team_b_possession, team_a_passes, team_b_passes, team_a_pass_accuracy, 
                    team_b_pass_accuracy, team_a_fouls, team_b_fouls, team_a_yellow_cards, team_b_yellow_cards, 
                    team_a_red_cards, team_b_red_cards, team_a_offsides, team_b_offsides, team_a_corners, 
                    team_b_corners, team_a_goal_times_str, team_b_goal_times_str])
        # Save statistics data to the database with the foreign key reference
       # save_statistics_to_database(stats_data)
        update_statistics_in_database(stats_data,1)

    else:
        print("pas passé")



def scroll_component(driver, element, repetitions=50):
    for _ in range(repetitions):
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)

def main():
    ascii_banner = pyfiglet.figlet_format("SCRAPING-FOOT")


    print(ascii_banner)
    global retry, max_retry
    retry += 1
    print(f"Attempt {retry} of {max_retry}")

    if retry > max_retry:
        print("Max retries exceeded.")
        return

    # Set up the database
    

    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.headless = False
      #  options.add_argument("--incognito")  # Ouvrir le navigateur en mode navigation privée
      #  options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)

        time.sleep(5)  # Attendre 5 secondes avant de charger l'URL

        
        # ty peux changer le pays ici 
        url = "https://www.google.com/search?q=liga"
        driver.get(url)

    
        # Attendre que l'élément intercepteur soit visible
        """
        intercepting_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.jsname="haAclf"'))
    )"""

    # Cliquer sur l'élément intercepteur pour le fermer ou le déplacer
       # intercepting_element.click()

    # Attendre que l'élément "Plus de matchs" soit cliquable
        more_btn = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-id="1"] > div[jsname="u9Pr0d"]'))
)
   # more_btn.click()

       # ActionChains(driver).move_to_element(more_btn).click().perform()
        driver.execute_script("arguments[0].click();", more_btn)

        main_div =WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jsname="jbF5N"].em0nhb'))
)
       # first_element =main_div[0] if main_div else None
        
        scroll_component(driver,main_div)
        time.sleep(2)

       

        #time.sleep(2)

        main_div = WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "OcbAbf"))
        )

        driver.execute_script("window.scrollBy(0, -500);")

        driver.execute_script("window.scrollBy(0, -500);")


        match_of_day = []
       

            

        for index, child_div in enumerate(main_div):
            """"
            if index == 0:
                continue 
            if index == 1:
                continue 
            if index == 2:
                continue 
            if index == 3:
                continue 
            """


            try:
                # Find the nested div with jsname="Tt3Dqc"
               # matchday_div = child_div.find_element(By.CSS_SELECTOR, 'div[jsname="Tt3Dqc"]')
                matchday_div = WebDriverWait(child_div, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jsname="Tt3Dqc"]')))
                # Get the value of the 'data-title' attribute
                day = matchday_div.get_attribute('data-title')
                day_text = matchday_div.get_attribute('data-title')
        # Check if the day_text contains "Journée" followed by a number
                if "Journée" in day_text:
                    day_number = day_text.split(" ")[-3]  # Get the number part
                   # print(f"day complet faux  est {day_text}")
                   # print(f"Jour: {day_number}")
                print("day complet compla est",day)
                if day:
                    match_of_day.append(day)
            except Exception as e:
                print("erruer",e)
                pass



            start_times = []
            try:
                # Find all nested divs with the class 'imso-loa imso-ani'
                nested_divs = child_div.find_elements(By.CSS_SELECTOR, 'div.imso-loa.imso-ani')
                for nested_div in nested_divs:
                    # Get the value of the 'data-start-time' attribute
                    start_time = nested_div.get_attribute('data-start-time')
                    if start_time:
                        start_times.append(start_time)
            except Exception as e:
                pass



            try:
                tables = child_div.find_elements(By.CLASS_NAME, 'KAIX8d')

                for i,table in enumerate(tables):
                    try:

                        time.sleep(2)
                        driver.execute_script("arguments[0].scrollIntoView();", table)

                        
                        driver.execute_script("arguments[0].click();", table)

                        time.sleep(3)
                        nGzje_elements = WebDriverWait(driver, 20).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "nGzje"))
                        )

                        nGzje_elements = WebDriverWait(driver, 20).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "nGzje"))
                        )

                        try:
                            driver.execute_script("window.history.go(-1)")
                            time.sleep(1)
                        except TimeoutException:
                            print("Back button was not found or clickable in the given time.")



                        # Store nGzje_elements HTML content in a file
                        nGzje_html = [element.get_attribute('outerHTML') for element in nGzje_elements]
                        if nGzje_html:
                            soup = BeautifulSoup(nGzje_html[0], 'html.parser')
                        else:
                            print("no soup")
   
                        


                        print("day est",day_text)
                        day = day_text
                        unix_timestamp = start_times[i]
                       # unix_timestamp =11122
                        date_string = unix_timestamp


                        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))

                                # Convertir l'objet datetime en timestamp Unix
                        timestamp = int(date_obj.timestamp())


                        extract_info_from_html(soup, day,timestamp)
                        time.sleep(2)
                      
                    except Exception as e:
                        print("ici une erreur",e)
                        pass

                        time.sleep(3)
            except NoSuchElementException:
                print("Table not found in the current child div.")




      

      

        
    except TimeoutException:
        print("Timeout: 'More' button not found.")
        driver.quit()
        return main()


           
        
       




    except Exception as e:
        print("An error occurred:", str(e))
        pass
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()