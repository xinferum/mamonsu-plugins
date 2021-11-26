# Mamonsu-plugins

Плагины для mamonsu - активного агента мониторинга Zabbix от компании PotgresPro - https://github.com/postgrespro/mamonsu

Документация по написанию и внедрению плагинов - [adding_custom_plugins](https://github.com/postgrespro/mamonsu/blob/master/documentation/adding_custom_plugins.md)

## Compatibility

Требуемая версия mamonsu 3+

## Plugins
Список плагинов:
- [pg_invalid_indexes.py](plugins/pg_invalid_indexes.py) - поиск в базах кластера невалидных индексов

**Update**: функционал плагина pg_invalid_indexes.py релизован в mamonsu версии [3.2.0](https://github.com/postgrespro/mamonsu/releases/tag/3.2.0), установка данного плагина начиная с 3.2.0 не требуется.

**pg_invalid_indexes.py**: отображает для каждой базы данных количество инвалидных индексов. Инвалидные или неготовые индексы могут возникать, например, при неуспешном создания индекса с использованием CONCURRENTLY, либо при неуспешном ребилде индекса с использованием CONCURRENTLY. Если количество инвалидных индексов не равно нулю - появляется алерт, критичность WARNING. Дискаверинг ведется по всем базам кроме бд postgres, mamonsu и шаблонных.

## License
Лицензия MIT, подробности в файле [LICENSE](LICENSE)
