import crcmod
import os
import qrcode
from django.conf import settings

class Payload():
    def __init__(self, nome, chavepix, valor, cidade, txtId):
        self.nome = nome
        self.chavepix = chavepix
        self.valor = f"{float(valor):.2f}"
        self.cidade = cidade
        self.txtId = txtId

        self.nome_tam = len(self.nome)
        self.chavepix_tam = len(self.chavepix)
        self.valor_tam = len(self.valor)
        self.cidade_tam = len(self.cidade)
        self.txtId_tam = len(self.txtId)

        self.merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{self.chavepix_tam}{self.chavepix}'

        self.payloadFormat = '000201'

        self.merchantAccount = f'26{len(self.merchantAccount_tam)}{self.merchantAccount_tam}'

        if self.valor_tam <= 9:
            self.trasactionAmount_tam = f'0{self.valor_tam}{self.valor}'
        else:
            self.trasactionAmount_tam = f'{self.valor_tam}{self.valor}'

        if self.txtId_tam <= 9:
            self.addDataField_tam = f'050{self.txtId_tam}{self.txtId}'
        else:
            self.addDataField_tam = f'05{self.txtId_tam}{self.txtId}'

        if self.nome_tam <= 9:
            self.nome_tam = f'0{self.nome_tam}'

        if self.cidade_tam <= 9:
            self.cidade_tam = f'0{self.cidade_tam}'

        self.merchantCategCod = '52040000'

        self.trasactionCurrency = '5303986'

        self.trasactionAmount = f'54{self.trasactionAmount_tam}'

        self.countryCode = '5802BR'

        self.merchantName = f'59{self.nome_tam}{self.nome}'

        self.merchantCity = f'60{self.cidade_tam}{self.cidade}'

        self.addDataField = f'62{len(self.addDataField_tam)}{self.addDataField_tam}'

        self.crc16 = '6304'

    def gerarPayload(self):
        # Monta o payload completo sem o CRC16 final
        self.payload = (
            f"{self.payloadFormat}"
            f"{self.merchantAccount}"
            f"{self.merchantCategCod}"
            f"{self.trasactionCurrency}"
            f"{self.trasactionAmount}"
            f"{self.countryCode}"
            f"{self.merchantName}"
            f"{self.merchantCity}"
            f"{self.addDataField}"
            f"{self.crc16}"
        )
        
        print("\nPayload (sem CRC):")
        print(self.payload)

        # Gera o CRC16
        self.gerarCrc16(self.payload)

    def gerarCrc16(self, payload):
        # Cria a função CRC16 para o padrão usado pelo PIX
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

        # Calcula o CRC16 e formata para maiúsculas
        self.crc16code = crc16(payload.encode('UTF-8'))
        self.crcCode_formatado = f"{self.crc16code:04X}"

        # Concatena o CRC16 para formar o payload completo
        self.payload_completa = f"{self.payload}{self.crcCode_formatado}"

        self.gerarQrCode()

        print("\nPayload (com CRC):")
        print(self.payload_completa)

    def gerarQrCode(self):
        # Cria o QR code a partir do payload completo
        self.qrCode = qrcode.make(self.payload_completa)

        # Define o caminho completo para salvar a imagem
        caminho_imagem = os.path.join(settings.MEDIA_ROOT, 'pix_qr_codes', 'pixqrcodegen.png')
        
        # Garante que o diretório exista
        os.makedirs(os.path.dirname(caminho_imagem), exist_ok=True)

        # Salva a imagem do QR code
        self.qrCode.save(caminho_imagem)

        # Retorna o caminho relativo para usar no template
        return os.path.join(settings.MEDIA_URL, 'pix_qr_codes', 'pixqrcodegen.png')

# class Payload():
#     def __init__(self, nome, chavepix, valor, cidade, txtId):

#         self.nome = nome
#         self.chavepix = chavepix
#         self.valor = f"{float(valor):.2f}"
#         self.cidade = cidade
#         self.txtId = txtId

#         self.nome_tam = len(self.nome)
#         self.chavepix_tam = len(self.chavepix)
#         self.valor_tam = len(self.valor.replace('.', ''))
#         self.cidade_tam = len(self.cidade)
#         self.txtId_tam = len(self.txtId)

#         self.merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{self.chavepix_tam}{self.chavepix}'

#         self.payloadFormat = '000201'

#         self.merchantAccount = f'26{len(self.merchantAccount_tam)}{self.merchantAccount_tam}'

#         if self.valor_tam <= 9:
#             self.trasactionAmount_tam = f'0{self.valor_tam}{self.valor}'
#         else:
#             self.trasactionAmount_tam = f'{self.valor_tam}{self.valor}'

#         if self.txtId_tam <= 9:
#             self.addDataField_tam = f'050{self.txtId_tam}{self.txtId}'
#         else:
#             self.addDataField_tam = f'05{self.txtId_tam}{self.txtId}'

#         if self.nome_tam <= 9:
#             self.nome_tam = f'0{self.nome_tam}'

#         if self.cidade_tam <= 9:
#             self.cidade_tam = f'0{self.cidade_tam}'

#         self.merchantCategCod = '52040000'

#         self.trasactionCurrency = '5303986'

#         self.trasactionAmount = f'54{self.trasactionAmount_tam}'

#         self.countryCode = '5802BR'

#         self.merchantName = f'59{self.nome_tam}{self.nome}'

#         self.merchantCity = f'60{self.cidade_tam}{self.cidade}'

#         self.addDataField = f'62{len(self.addDataField_tam)}{self.addDataField_tam}'

#         self.crc16 = '6304'

#     def gerarPayload(self):
#         self.payload = f'{self.payloadFormat}{self.merchantAccount}{self.merchantCategCod}{self.trasactionCurrency}{self.trasactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}'

#         print()
#         print(self.payload)
#         print()

#         self.gerarCrc16(self.payload)

#     def gerarCrc16(self, payload):
#         crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

#         self.crc16code = hex(crc16(str(payload).encode('UTF-8')))

#         self.crcCode_formatado = ((str(self.crc16code)).replace('0x', '')).upper()

#         self.payload_completa = f"{self.payload}{self.crcCode_formatado}"

#         print(f"CRC16 Code: {self.payload_completa}")

#     def exibirPayloadCompleto(self):
#         if not self.crc16code:
#             self.gerarPayload()
#         payload_completo = f"{self.payload}{self.crcCode_formatado}"
#         print(f"Payload completo: {payload_completo}")
#         return payload_completo

#     def __repr__(self):
#         return (
#             f"Payload(nome={self.nome}, chavepix={self.chavepix}, valor={self.valor}, "
#             f"cidade={self.cidade}, txtId={self.txtId})"
#         )

# Teste da classe
# pix_payload = Payload("Pedro Correa", "38455378840", "5.00", "Rio", "Sonart")
# pix_payload.gerarPayload()
# pix_payload.exibirPayloadCompleto()
    

# def calcular_crc16(payload):
#     polynomial = 0x1021
#     crc = 0xFFFF
#     bytes_data = payload.encode('utf-8')
#     for b in bytes_data:
#         crc ^= b << 8
#         for _ in range(8):
#             if (crc & 0x8000) != 0:
#                 crc = ((crc << 1) ^ polynomial) & 0xFFFF
#             else:
#                 crc = (crc << 1) & 0xFFFF
#     return format(crc, '04X')

# def montar_payload_pix(chave_pix, nome_merchant, cidade_merchant, valor, referencia='***'):
#     valor_str = f"{valor:.2f}".replace(',', '.')

#     # Montando Merchant Account Information (tag 26)
#     merchant_info_value = f"0014BR.GOV.BCB.PIX01{chave_pix}"
#     merchant_info = f"26{len(merchant_info_value):02}{merchant_info_value}"

#     # Montando outros campos
#     payload = (
#         "00" "02" "01"  # Payload Format Indicator
#         "01" "02" "12"  # Point of Initiation Method (12 = dinâmico)
#         + merchant_info +
#         "52" "04" "0000" +  # Merchant Category Code
#         "53" "03" "986" +   # Currency (BRL)
#         "54" f"{len(valor_str):02}" + valor_str +  # Valor
#         "58" "02" "BR" +    # País
#         "59" f"{len(nome_merchant):02}" + nome_merchant +
#         "60" f"{len(cidade_merchant):02}" + cidade_merchant +
#         "62" f"{len('05' + referencia):02}" + "05" + referencia +
#         "63" "04"  # CRC placeholder
#     )

#     crc = calcular_crc16(payload)
#     return payload + crc

# # Teste:
# print(montar_payload_pix("38455378840", "Pedro Correa", "Rio Preto", 0.05))

# def gerar_qr_code_url(payload_pix):
#     qr = pyqrcode.create(payload_pix)
#     buffer = io.BytesIO()
#     qr.png(buffer, scale=8)
#     img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
#     return f"data:image/png;base64,{img_str}"