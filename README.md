# BH Escape
Projeto da Sala Santos Dumont
## Principais commit's:
Conclusão da programação da lógica antiga com painel de controle web funcionando:
* [Programação HTML e CSS, criação de métodos na views deixando Painel de controle HTML funcional](https://github.com/guilhermerodrigues680/escapebh/tree/6d374ad6dd71f9a5e68928283a25675a0c69ad9c)

![LOGO BH Escape](https://github.com/guilhermerodrigues680/escapebh/raw/6d374ad6dd71f9a5e68928283a25675a0c69ad9c/escapebhserver/escapebhjogo/static/imagens/logo.png)

## Instruções
Comando para instalar pacotes do pip:

```shell
# Criar venv
python3 -m venv escapebhvenv
# Instalar ou atualizar pip (Gerenciador de pacotes python)
python3 -m pip install --upgrade pip
# O arquivo "requirements.txt" guarda as dependências que serão instaladas utilizando o pip install
pip install -r requirements.txt
```

### Iniciando script no shell
Encerrar execucao com `sudo fuser -k 8000/tcp `
executar `. /home/pi/escapebh/escapeiniciar`

**Pacotes no requirements.txt :**
- Django~=2.0.6
- smbus
- RPi.GPIO
- spidev

## Bibliotecas
**RFID MFRC522 (RFID-RC522)**
- https://github.com/mxgxw/MFRC522-python
- https://github.com/pimylifeup/MFRC522-python


## Fazendo Commit
- Verificar se a branch trava-magnetica está selecionada `git branch'
- Adicionar todas as mudanças/arquivos com `git add *`
- Comitar mudancas com comentario `git commit -m 'COMENTARIO'`
- Enviar alteracoes com `git push origin trava-magnetica`
