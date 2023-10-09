Тестовое задание на позицию python разработчик.
```
Что было сделано:
*Ознакомление с документацией проекта по средством Swagger(OpenAPI).
*Изменение структуры проекта:
   Создание отдельного модуля api_v0 и разбиение его на сущности(City, Picnic, User, PicnicRegistration)
   Пример шаблона для каждой сущности в api_v0:



  ==============ПОЛНОЕ ОПИСАНИЕ ТОЛЬКО ДЛЯ СУЩНОСТИ City ДАЛЕЕ ВСЕ СУЩНОСТИ НАСЛЕДУЮТ ОДИНАКОВУЮ ЛОГИКУ АРХИТЕКТУРЫ===========
```   
fastapi-project
├── src
│   ├── api_v0
│   │   ├── __init__.py   # Инициализатор пакета, где все роутеры собираются для последуещего импорта в эеземпляр fastapi(app)
│   │   ├── City 
|   |   |   └──  Weather # Сущность погоды для города
|   |   |   |   ├── weather_get.py             # Функция получения погоды.
|   |   |   ├── check_exist_city.py            # Проверка существования города.
│   │   |   ├── router.py                      # Роутеры для сущности City
|   |   |   ├── schemas.py                     # Pydantic schemas
|   |   |   ├── dependencies.py                # Зависимости для сущности City
│   │   |   ├── crud.py                        # Create Read Update Delete операции для сущности City.
│   │   ├── Picnic
│   │   |   ├── router.py
|   |   |   ├── schemas.py  
|   │   │   ├── crud.py
│   │   ├── User
│   │   |   ├── router.py
|   |   |   ├── schemas.py
|   |   |   ├── dependencies.py    
|   │   │   ├── crud.py
│   │   ├── PicnicRegistration
│   │   |   ├── router.py
|   |   |   ├── schemas.py
|   |   |   ├── crud.py    
|   │   │   ├── service.py 
|   ├── models
│   │   ├── __init__.py                     # Инициализация всех элементов для работы с БД через SQLalchemy.
│   │   ├── db_config.py                    # Создание AsyncEngine, AsycSessionFactory, SCOPED_SESSION(в пределах current_task), Generator for recieve async session obj in current scope.
│   │   ├── db_model_base.py                # Базовая подель от sqlahcmey.orm DeclarativeBase с @declarative_attr.derective(как @property) для имени таблицы, и поелем ID(UUID).
│   │   ├── db_model_city.py
│   │   ├── db_model_picnic.py
│   │   ├── db_model_user.py
│   │   ├── db_model_picnic_registration.py
|   ├── main.py
|   ├── config.py 
├── tests(not realized yet)
 y для api_v0, для повышения читабельности кода, удобства импорта и масштабируемости)
```

```
*Добавлен поиск городов аргументом q(Query obj fastapi) в запросе get_city
*Добавлена возможность фильтрации пользователей по максимальному и минимальному возрасту(в запросе к всем юзерам)
*Добавлена логика регистраци на пикник.
*Произведен рефакторинг external_requests.py
*Проблемы при масштабировании проекта учтены при создании архитектуры проекта.
*Приведены к нормальному виду Методы обращения к endpoints их название и пити обращения к ним.
*Описано вся логика работы через Swagger и в readmi.md file на github.
*Оптимизирован запрос к БД для получения пикников и их юзеров(За место joinload выбран selectinload(для создания отдельного запроса) так как связь to many.
*Здесь описана правильная архитектура проекта и создана. 
*Каждое логическое действие описано комминтарием(docstingss для функций и классов)
   
