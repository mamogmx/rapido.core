
class RuleAssignee:

    @property
    def assigned_rules(self):
        return self.annotation.get('assigned_rules', [])

    def assign_rules(self, rules):
        old_rules = self.assigned_rules
        self.annotation['assigned_rules'] = rules
        for rule_id in set(old_rules + rules):
            self.refresh_rule(rule_id)

    def remove_rule(self, rule_id):
        if rule_id in self.assigned_rules:
            rules = [id for id in self.assigned_rules
                if id!=rule_id]
            self.annotation['assigned_rules'] = rules
            self.refresh_rule(rule_id)

    def refresh_rule(self, rule_id):
        annotation = self.annotation
        if rule_id not in annotation['assigned_rules']:
            if annotation.has_key(rule_id + '_code'):
                del annotation[rule_id + '_code']
            if annotation.has_key('compiled_' + rule_id + '_code'):
                del annotation['compiled_' + rule_id + '_code']
        else:
            db = self.database
            rule = db.rules().get(rule_id)
            if not rule:
                return
            annotation[rule_id + '_code'] = rule['code']
            annotation['compiled_' + rule_id + '_code'] = None
