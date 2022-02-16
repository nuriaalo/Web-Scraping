from selenium import webdriver
import pandas as pd

web = 'https://www.amazon.es/'

driver_path = 'C:\chromedriver_win32/chromedriver'

driver = webdriver.Chrome(driver_path)
driver.get(web)

# click cookies button
cookies_button = driver.find_element_by_id('sp-cc-accept')
cookies_button.click()

# elemento a buscar
keyword = "tarjeta grafica"
search = driver.find_element_by_id('twotabsearchtextbox')
search.send_keys(keyword)

# click search button
search_button = driver.find_element_by_id('nav-search-submit-button')
search_button.click()

# click precio entre 50 y 100
precio_button = driver.find_element_by_xpath('//*[@id="p_36/1323857031"]/span/a/div/label/i')

precio_button.click()

# click seleccionar el orden
orden_button = driver.find_element_by_id('a-autoid-0')
orden_button.click()

# click valoracion de clientes
valoracion_button = driver.find_element_by_id('s-result-sort-select_3')
valoracion_button.click()

items = driver.find_elements_by_xpath('//div[contains(@class, "s-result-item s-asin")]')

lista_productos = []
count = 0

for item in items:
	#obtenemos los 10 primeros
	if count < 10:
	# solo se añade a la lista si no es patrocinado
		patrocinado = item.find_elements_by_xpath('.//div[@class="a-row a-spacing-micro"]/span')
		if patrocinado == []:
		
			#nombre
			nombre = item.find_element_by_xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]').text
		
			#precio
			precio = item.find_elements_by_xpath('.//span[@class="a-price-whole"]')
			if precio != []:
				precio = precio[0].text
			else:
				precio= '-'
		
			#valoración
			ratings = item.find_elements_by_xpath('.//div[@class="a-row a-size-small"]/span')
			if ratings != []:
				rating = ratings[0].get_attribute('aria-label')
			else:
				rating = '-'

			#caracteristicas
			caracteristicas = item.find_elements_by_xpath('.//span[@class="a-text-bold"]')
			if caracteristicas != []:
				tam = caracteristicas[0].text
				tipo = caracteristicas[1].text
				tarjeta = caracteristicas[2].text
				velocidad = caracteristicas[3].text
			else:
				tam = '-'
				tipo = '-'
				tarjeta = '-'
				velocidad = '-'
			
		else:
			break
	
		producto={
				'Nombre':nombre,
				'Precio':precio,
				'Valoracion':rating,
				'Tamaño RAM':tam,
				'Tipo RAM':tipo,
				'Tarjeta':tarjeta,
				'Velocidad':velocidad
				}
	
		lista_productos.append(producto)
		count+=1

driver.quit()

# creo el dataframe
df = pd.DataFrame({'Tarjetas': lista_productos})
# creo el csv
df.to_csv('tarjetas.csv', index=False)
