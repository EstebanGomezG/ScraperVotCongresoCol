from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def main():
    service= Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1080,720")
    driver = webdriver.Chrome(service=service, options=option)
    driver.get("https://congresoalamano.elespectador.com/proyecto-perfil/220004/")
   
    try:
        wait = WebDriverWait(driver, 10)
        contenedor = wait.until(EC.presence_of_element_located((By.ID, 'Votacion2')))
        
    
    except TimeoutError:
        print("El contenedor con id 'Votacion2' no se encontró dentro del tiempo especificado.")
        driver.quit()

    elementos_votacion = contenedor.find_elements(By.CLASS_NAME, 'ProjectList-ItemDescription')
    print(len(elementos_votacion))

    datos = []

    for elemento in elementos_votacion:
        try:
            voto_element = elemento.find_element(By.CLASS_NAME, 'ProjectList-ItemValue')
            voto = voto_element.text.strip()
            
            nombre_element = elemento.find_element(By.CLASS_NAME, 'ProjectList-ItemName')
            nombre = nombre_element.text.strip()
            
            if voto.lower() in ['si', 'sí']:
                voto_normalizado = 'Sí'
            elif voto.lower() == 'no':
                voto_normalizado = 'No'
            elif voto.lower() in ['au', 'ausente', 'ausente']:
                voto_normalizado = 'Ausente'
            else:
                voto_normalizado = voto
            
            datos.append({'Nombre': nombre, 'Voto': voto_normalizado})
            
        except Exception as e:
            print(f"Error al procesar un elemento: {e}")

    df = pd.DataFrame(datos)

    print(df.head())
    
    df.to_csv('votaciones_senadores.csv', index=False, encoding='utf-8-sig')

    print("Datos exportados exitosamente a 'votaciones_senadores.csv'")
    driver.quit()
            

if __name__ == "__main__":
    main()