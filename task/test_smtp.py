import smtplib

def test_smtp_connection(host, port, use_tls=True, username=None, password=None):
    try:
        server = smtplib.SMTP(host, port)
        server.set_debuglevel(1)  # Включаем отладку для вывода подробной информации
        if use_tls:
            server.starttls()
        if username and password:
            server.login(username, password)
        print("Подключение успешно установлено")
        server.quit()
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_smtp_connection(
        host="smtp.gmail.com",  # Используйте правильное имя хоста
        port=587,
        use_tls=True,
        username="your_email@gmail.com",  # Ваш email
        password="your_email_password"  # Пароль от вашего email
    )