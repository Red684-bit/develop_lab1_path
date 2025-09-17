#!/usr/bin/env python
import os
import sys
import django
from django.test import Client
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab1.settings')

try:
    django.setup()
except Exception as e:
    print(f"Ошибка при настройке Django: {e}")
    sys.exit(1)

settings.ALLOWED_HOSTS.extend(['testserver', 'localhost', '127.0.0.1'])

def run_test(test_func, test_name):
    try:
        test_func()
        print(f"   ✅ {test_name} - OK")
        return True
    except Exception as e:
        print(f"   ❌ {test_name} - Ошибка: {e}")
        return False

def test_lab():
    client = Client()
    tests_passed = 0
    total_tests = 0

    print("🧪 Запуск автоматической проверки лабораторной работы...\n")
    print("⚠️  Убедитесь, что сервер разработки (runserver) НЕ запущен!\n")

    tests = [
        {
            'name': 'Главная страница',
            'func': lambda: test_main_page(client),
            'points': 1
        },
        {
            'name': 'Страница книги (существующая)',
            'func': lambda: test_existing_book(client),
            'points': 1
        },
        {
            'name': 'Страница книги (несуществующая, 404)',
            'func': lambda: test_nonexistent_book(client),
            'points': 1
        },
        {
            'name': 'Поиск с параметрами',
            'func': lambda: test_search_with_params(client),
            'points': 1
        },
        {
            'name': 'Установка темы и переадресация',
            'func': lambda: test_theme_redirect(client),
            'points': 1
        },
        {
            'name': 'Динамическая маршрутизация (re_path)',
            'func': lambda: test_review_detail(client),
            'points': 2
        }
    ]

    for test in tests:
        total_tests += 1
        print(f"{total_tests}. {test['name']}...")
        if run_test(test['func'], test['name']):
            tests_passed += 1

    print("\n" + "="*60)
    print(f"РЕЗУЛЬТАТ: {tests_passed}/{total_tests} тестов пройдено")
    
    if tests_passed == total_tests:
        print("🎉 Поздравляем! Все тесты пройдены успешно!")
        print("✅ Ваша работа соответствует требованиям. Можно сдавать!")
    else:
        print(f"😥 Не пройдено тестов: {total_tests - tests_passed}")
        print("💡 Подсказка: Читайте сообщения об ошибках выше для понимания проблемы.")
    print("="*60)

    return tests_passed == total_tests

def test_main_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200, f"Код ответа {response.status_code}, ожидался 200"
    content = response.content.decode('utf-8')
    assert "Главная страница сайта" in content, "Не найдена строка на главной"

def test_existing_book(client):
    """Тест страницы существующей книги"""
    response = client.get('/book/1/')
    assert response.status_code == 200, f"Код ответа {response.status_code}, ожидался 200"
    content = response.content.decode('utf-8')
    assert "Анна Каренина" in content, f"Не найдено название книги. Контент: {content}"

def test_nonexistent_book(client):
    """Тест страницы несуществующей книги"""
    response = client.get('/book/999/')
    assert response.status_code == 404, f"Код ответа {response.status_code}, ожидался 404"
    content = response.content.decode('utf-8')
    assert "Книги нет" in content, f"Не указана ошибка"

def test_search_with_params(client):
    """Тест поиска с параметрами"""
    response = client.get('/search/?q=Толстой&type=author')
    assert response.status_code == 200
    content = response.content.decode('utf-8')
    assert "Толстой" in content and "author" in content, "Параметры поиска не обработаны"
    response2 = client.get('/search/')
    assert response2.status_code == 200

def test_theme_redirect(client):
    """Тест установки темы и переадресации"""
    response = client.get('/set_theme/?color=dark', follow=True)
    assert len(response.redirect_chain) > 0, "Не произошло переадресации"
    assert response.status_code == 200
    content = response.content.decode('utf-8')
    assert "dark" in content, "Тема не была установлена или не отображается"

def test_feedback_routes(client):
    """Тест вложенных маршрутов"""
    response = client.get('/feedback/')
    assert response.status_code == 200
    content = response.content.decode('utf-8')
    assert "Форма обратной связи" in content
    
    response_thanks = client.get('/feedback/thanks/')
    assert response_thanks.status_code == 200
    content_thanks = response_thanks.content.decode('utf-8')
    assert "Спасибо за отзыв" in content_thanks

def test_review_detail(client):
    """Тест динамической маршрутизации с re_path"""
    response = client.get('/book/du-312/reviews/42/')
    assert response.status_code == 200, f"Код ответа {response.status_code}, ожидался 200"
    content = response.content.decode('utf-8')
    assert "Отзыв #42 к книге 'du-312'" in content, f"Неверный контент. Получено: {content}"

if __name__ == '__main__':
    test_lab()