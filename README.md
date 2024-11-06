# ХАКАТОН от<br>[ОМК-ИТ](https://habr.com/ru/companies/omk-it/articles/850434/?telegram_habr)
Цель проекта: создание решения на основе большой языковой модели для работы с нормативно-техническими документами (ГОСТ), их анализа и поиска информации по пользовательскому запросу.

[1. Описание предлагаемого решения](#краткое-описание)

[2. Работа с приложением](#использование-приложения)

&emsp; [2.1. В Телеграм-боте (способ 1, самый простой)](#в-ТГ)

&emsp; [2.2. На локальном сервере (способ 2)](#на-локальном-сервере)

[3. Структура репозитория, описание работы модулей](#подробное-описание-структуры-репозитория)

[4. Авторы](README.md#команда)

## Краткое описание

Для существенного ускорения работы llm и построенного на ее основе приложения, а также возможности использования меньших моделей (до 40b), обработка пользовательского запроса разделена на несколько этапов:

- шаг 1: определение в пользовательском запросе номера НТД (ГОСТа) для поиска в БД текстовых фрагментов, относящихся только к этому документу;

- шаг 2: определение в каком типе данных следует искать информацию по пользовательскому запросу (текстовая, табличная или графическая информация);

- шаг 3: в зависимости от результатов предыдущего шага:
    * для текстовой информации - поиск в векторной базе данных и составление некоторой выборки по ближайшему расстоянию эмбедингов слов запроса и находящейся в БД текстовой информации из ГОСТ;
    * для табличной информации - анализ с помощью llm метаданных по табличным данным ГОСТа, выбор моделью набора таблиц для последующего анализа;
    * для графической информации - анализ словесного описания графических объектов, сделанного с помощью модели image-to-text (пока не реализовано, в перспективе);

- шаг 4: финальный анализ полученной на предыдущем шаге выборки данных (текстовых блоков или таблиц), генерация ответа на поставленный вопрос;

- шаг 5: вывод ответа на вопрос (сделано), а также фрагмента(ов) из нормативного документа, послужившего(их) основой для подготовки ответа для дополнительной верификации (вторая часть в перспективе доработки);

Парсинг нормативно-технических документов и их запись в БД осуществляется автоматически с помощью llm. Парсинг текста, табличных данных и графической информации осуществляется отдельно друг от друга. Для текстовой информации модель разбивает входные данные на логически обособленные блоки, которые затем заносятся в векторную БД (Chromadb), с взаимным перекрыванием. При обработке табличных данных модель составляет метаинформацию по каждой таблице, указывая идентификационные обозначения столбцов, строк таблицы, а также перечень уникальных значений, например:
```
{
"Название таблицы": "Таблица 1 - механические свойства проката",
"Толщина проката, мм": ["до 20", "21-40"],
"Временное сопротивление, Н/мм2 (кгс/мм2)": ["430(44)"],
"Предел текучести, Н/мм2 (кгс/мм2)": ["295(30)"],
"Относительное удлинение, %": ["16"],
"Ударная вязкость KCU, Дж/см2  (кгс·м/см2)": ["39(4)", "29(3)"],
"Изгиб до параллельности сторон (- толщина, диаметр оправки)": ["=4", "=5"]
}
```
Метаинформация также заносится в БД и используется для предварительного поиска нужных таблиц в соответствии с пользовательским запросом.

## Использование приложения

### В ТГ

На период проведения Хакатона приложение развёрнуто в виде [Телеграм-бота](https://t.me/RadostTrudaMetalloInfoBot). В боте можно ввести интересующий вопрос по двум ГОСТам (которые были обозначены в правилах Хакатона) и получить ответ.

Репозиторий с ботом и всеми необходимыми для его работы файлами (БД и т.д.) расположено [здесь](https://github.com/chetverovod/MetalloInfoBot).


### На локальном сервере

Приложение можно развернуть локально. Для этого необходимо воспользоваться [другим репозиторием](https://github.com/YaRoLit/MetalloHakaton.git). В таком случае оно не содержит GUI, работа с приложением осуществляется через командную строку. 
```
$ git clone git@github.com:YaRoLit/MetalloHakaton.git
```
Установите необходимые для работы приложения библиотеки python:
```
$ cd MetalloHakaton && pip install -r requirements.txt 
```
Запустите приложение:
```
$ python3 main.py
```
На странице проекта расположен файл Jupyter notebook с [с возможностью отправки запросов](main_test.ipynb), в котором имеется пример вызова метода ответов на вопросы по ГОСТу. 

## Подробное описание структуры репозитория

Репозиторий для локального развертывания содержит следующие папки и файлы. Основные файлы:
Каталог src:
- [модуль](src/docx_parse.py) для парсинга нормативно-технических документов из docx файлов с записью в векторную БД chromatab.

- [модуль](src/llama_model_api.py) для работы с llm. Внимание! Нами используется языковая модель [Qwen-2.5 14b](https://huggingface.co/bartowski/Rombos-LLM-V2.6-Qwen-14b-GGUF) с квантизацией Q3-K-M. Файлы модели в репозитории не содержатся из-за большого объема, вы можете загрузить их по приведенной ссылке.

- [модуль](src/vbd_api.py) для работы с векторной базой данных chromadb.

- [модуль](src/embd_func.py) токенизатора эмбеддингов базы данных.

- [модуль](src/chain_of_thoughts.py) "цепь рассуждений" для реализации вышеописанного алгоритма из 5 шагов для генерации ответа на пользовательский запрос.

Корневой каталог:
- [модуль](main.py) для запуска приложения с работой через командную строку.

- [модуль](docx-parser.py) для парсинга документов docx в БД

- модули *.ipynb с примерами использования.

## Команда
<p align="center">
<img src = './images/logo.png' alt = 'Team logo' align='center'/>
</p>

Игорь Пластов ([chetverovod](https://github.com/chetverovod)): создание ТГ-бота, обработка текстовых данных, создание векторной базы данных, эксперименты с llm, финальная сборка проекта. 
Ярослав Литаврин ([YaRoLit](https://github.com/yarolit)): обработка табличных данных, эксперименты с llm, подготовка standalone версии.
