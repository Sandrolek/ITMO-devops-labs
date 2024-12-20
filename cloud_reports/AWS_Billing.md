
# Лабораторная работа 1. Знакомство с IaaS, PaaS, SaaS сервисами в облаке на примере Amazon Web Services (AWS). Создание сервисной модели.

## Задание

### Цель работы: 

Знакомство с облачными сервисами. Понимание уровней абстракции над инфраструктурой в облаке. Формирование понимания типов потребления сервисов в сервисной-модели. 


### Дано: 

Слепок данных биллинга от провайдера после небольшой обработки в виде SQL-параметров. Символ % в начале/конце означает, что перед/после него может стоять любой набор символов.

Образец итогового соответствия, что желательно получить в конце. В этом же документе  

### Необходимо: 

Импортировать файл .csv в Excel или любую другую программу работы с таблицами. Для Excel делается на вкладке Данные – Из текстового / csv файла – выбрать файл, разделитель – точка с запятой.

Распределить потребление сервисов по иерархии, чтобы можно было провести анализ от большего к меньшему (напр. От всех вычислительных ресурсов Compute дойти до конкретного типа использования - Выделенной стойка в датацентре Dedicated host usage).

Сохранить файл и залить в соответствующую папку на Google Drive.

### Алгоритм работы: 

Сопоставить входящие данные от провайдера с его же документацией. Написать в соответствие колонкам справа значения 5 колонок слева, которые бы однозначно классифицировали тип сервиса. Для столбцов IT Tower и Service Family значения можно выбрать из образца.

## Выполнение работы

На основе документации AWS была заполнена таблица, распределены IT Towers&Service Family из примера.

Также доступно по [ссылке](https://docs.google.com/spreadsheets/d/1APUiX-jnBX_BIRx2991oHUj0_RT6bmdf/edit?usp=sharing&ouid=110913290843078262056&rtpof=true&sd=true)

![Result](/cloud_reports/images/table.png)

Пока я работал с документацией, выделил следующие сервисы от AWS:

- **Amazon CloudWatch**

Собирает метрики использования приложений, развернутых в AWS. Собирает метрики, ведет журналы и поддерживает создание кастомных алертов.

Также предоставляет свое API, с помощью которого можно настроить собственные системы мониторинга на базе мониторинга AWS.

- **AWS Budgets**

Управляет затратами и распределением ресурсов в AWS. Позволяет настроить алерты при превышении заданных лимитов, что обеспечивает высокую денежную эффективность.

- **AWS Device Farm**

Дает возможность тестирования мобильный и веб-приложений на реальных устройствах.
- **AWS Lambda**

Serverless часть AWS для запуска кода внутри своих функций. Автоматически масштабируется, что позволяет оплачивать лишь ресурсы, затраченные на конкретную задачу.

- **Amazon EMR (Elastic MapReduce)**

Предоставляет управляемые кластеры для работы с большими данными, предлагает ряд инструментов, таких как Hadoop, Spark, идр.

- **Amazon Elastic Compute Cloud (Amazon EC2)**

Один из главных сервисов, позволяет запускать вм, управлять ими. Общим словом - предоставляет масштабируемые вычислительные мощности в облаке.

- **Amazon WorkMail**

Защищенная корпоративная почта.

- **Amazon WorkSpaces**

Виртуальные рабочие столы в облаке - сделано для удобства пользователей, чтоб совместить привычные условия работы и наличие всех доступов.

- **Alexa for Business (A4B)**

Собственный менеджер AWS для создания конференций, созвонов и так далее. Автоматизированный PM, если так можно сказать)

- **Amazon Detective**

Анализирует угрозы инфраструктуре, выявляет какие-либо спорные ситуации и тп.

- **Amazon Macie**

Автоматические обнаруживает конфиденциальные данные в хранилищах AWS, помогает выявлять утечки информации.

- **Amazon Pinpoint**

Обеспечивает взаимодействие с пользователями через электронные письма, SMS и пуши.

- **Amazon Mobile Analytics**

Предоставляет инструменты для анализа поведения пользователей мобильных приложений.

## Выводы

Были подробно изучены сервисы AWS, проанализированы некоторые их применения на конкретных примерах.