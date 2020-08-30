import bs4
import requests
import smtplib
import time

headers = {'referer': 'https://www.google.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

def mercadoPrice(productUrl):
    res = requests.get(productUrl, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    discount = soup.find('div', class_='price-tag discount-arrow arrow-left')
    elems = soup.find('span', class_='price-tag')
    pricen_str = elems.text.strip()
    pricen_str = pricen_str.replace('.', '') # se for mais que 1.000,00
    pricen_str = pricen_str.replace(',', '.')
    pricen_str = pricen_str.replace('\n', '')
    price = float(pricen_str[2:])
    if discount != None:
        discount = discount.text.strip()
        discount = float(discount[:2])/100
        price = price * (1-discount)
    return price

def sendEmail(price, productUrl):
    res = requests.get(productUrl, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    title = soup.title.text.strip()
    conn = smtplib.SMTP('smtp.gmail.com', 587) # Se o seu email for do gmail
    conn.ehlo() 
    conn.starttls() 
    conn.login('COLOQUE SEU EMAIL AQUI', 'COLOQUE SUA SENHA AQUI') # Email e senha
    from_ = 'COLOQUE SEU EMAIL AQUI'
    to_ = 'COLOQUE SEU EMAIL AQUI (DE NOVO)'
    subject = '{} abaixo do preço estipulado!'.format(title)
    body = '{} está a R${} no momento.\nConfira no link: {}\n\n-Mercado Livre Price Bot'.format(title, price, productUrl)
    msg = 'Subject: {}\n\n{}'.format(subject, body)
    conn.sendmail(to_, from_, msg.encode('utf-8'))
    print('Email has been sent!')
    conn.quit()

def checkPrice(itens):
    for item in itens:
        if item['email'] != True:
            price = mercadoPrice(item['url'])
            if price < item['price']:
                sendEmail(price, item['url'])
                item['email'] = True

# Itens Mercado Livre:
# Aqui você pode adicionar quantas URL's quiser, aqui somente alguns exemplos
radiador = 'https://produto.mercadolivre.com.br/MLB-1223673814-radiador-ar-quente-ford-fiesta-ka-1998-2004-courier-_JM?matt_tool=86155663&matt_word&quantity=1'
vent = 'https://produto.mercadolivre.com.br/MLB-688536851-eletro-ventilador-ventoinha-9-polegadas-universal-soprante-_JM?quantity=1#reco_item_pos=3&reco_backend=machinalis-v2p-pdp-v2&reco_backend_type=low_level&reco_client=vip-v2p&reco_id=c9043c36-1a19-42a8-ab37-bfde8edffff0'
bomba = 'https://produto.mercadolivre.com.br/MLB-1070042334-bomba-de-combustivel-universal-uno-mille-fire-evo10-14flex-_JM#position=2&type=item&tracking_id=e047c1cc-7b24-4052-bf7e-a5159243201b'
refil = 'https://produto.mercadolivre.com.br/MLB-1180368585-refil-bomba-de-combustivel-yamaha-fazer-150-codigo-10180-_JM#position=3&type=item&tracking_id=3f833210-522e-478e-a237-2efc1a0f915a'

# Não se esquaça de também adicionar o item aqui, junto com o preço
itens = [{'url': radiador, 'price': 160, 'email': False, 'store': 'mercado'}, #'price': preço máximo para o email ser enviado
         {'url': vent, 'price': 100, 'email': False, 'store': 'mercado'},
         {'url': bomba, 'price': 130, 'email': False, 'store': 'mercado'},
         {'url': refil, 'price': 65, 'email': False, 'store': 'mercado'}]

while(True):

    checkPrice(itens) # Aqui é o tempo em que o programa irá rodar; no momento está em 1 hora (3600s)
    time.sleep(3600)
