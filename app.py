from website import create_app

app = create_app()

# aplikacja sie wystaruje tylko wtedy kiedy ja wystartuje ten plik
# zabezpiecza to przypadek w ktorym bym importowal 'main.py' a ta by sie chciala wystartowac
if __name__ == '__main__':
    # debug = true - za kazdym razem kiedy wprowadze zmiane w kodzie serwer sie zresetuje i pokaze zmiany
    app.run(debug=True, host="192.168.12.53") 
    # Serwer startuje w lokalnej sieci, udostępnia możliwość uruchomienia strony na telefonach i innych urządeniach w tej samej sieci. (IP for change)
