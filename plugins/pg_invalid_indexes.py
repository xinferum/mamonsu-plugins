# -*- coding: utf-8 -*-

from mamonsu.plugins.pgsql.plugin import PgsqlPlugin as Plugin
from mamonsu.plugins.pgsql.pool import Pooler

class PgInvalidIndexes(Plugin):
    Interval = 60
    
    DEFAULT_CONFIG = {
        'Interval': str(60), # Default interval (1 hour = 3600 sec)
    }

    zbx_key = "invalid_indexes_count"

    # 
    query_agent_discovery = "SELECT json_build_object ('data',json_agg(json_build_object('{#TABLE_IDX}', '" + zbx_key + "')));"

    # Select count on invalid indexes in database
    query = """
        SELECT COUNT(*)
        FROM pg_index i
        JOIN pg_class c ON i.indexrelid = c.oid
        JOIN pg_class c2 ON i.indrelid = c2.oid
        JOIN pg_namespace n2 ON c2.relnamespace = n2.oid
        WHERE (NOT i.indisready OR NOT i.indisvalid)
        AND NOT EXISTS (SELECT 1 FROM pg_stat_activity where datname = current_database() AND query ilike '%concurrently%' AND pid <> pg_backend_pid());
        """

    AgentPluginType = 'pg'
    key_rel_part = 'pgsql.' + zbx_key
    key_rel_part_discovery = key_rel_part+'{0}'

    def run(self, zbx):
        objects = []
        for info_dbs in Pooler.query("select datname from pg_catalog.pg_database where datistemplate = false and datname not in ('mamonsu','postgres')"):
            objects.append({'{#TABLE_IDX}': info_dbs[0]})
            result = Pooler.query(self.query, info_dbs[0])
            zbx.send(self.key_rel_part+'[{0}]'.format(info_dbs[0]), result[0][0])            
        zbx.send(self.key_rel_part+'[]', zbx.json({'data': objects}))

    def discovery_rules(self, template, dashboard=False):
        rule = {
            'name': 'Invalid indexes in database discovery',
            'key': self.key_rel_part_discovery.format('[{0}]'.format(self.Macros[self.Type])),
            'filter': '{#TABLE_IDX}:.*'
        }
        items = [
            {'key': self.right_type(self.key_rel_part_discovery, var_discovery="{#TABLE_IDX},"),
             'name': 'Invalid indexes in database: {#TABLE_IDX}',
             'units': Plugin.UNITS.none,
             'value_type': Plugin.VALUE_TYPE.numeric_unsigned,
             'delay': self.Interval},
        ]
        conditions = [
            {
                'condition': [
                    {'macro': '{#TABLE_IDX}',
                        'value': '.*',
                        'formulaid': 'A'}
                ]
            }
        ]        
        triggers = [{
                    'name': 'PostgreSQL: In the database {#TABLE_IDX} invalid indexes on {HOSTNAME} (value={ITEM.LASTVALUE})',
                    'expression': '{#TEMPLATE:'+self.right_type(self.key_rel_part_discovery, var_discovery="{#TABLE_IDX},")+'.last()}&gt;0',
                    'priority': 2
                    }
        ]
        return template.discovery_rule(rule=rule, conditions=conditions, items=items, triggers=triggers)
