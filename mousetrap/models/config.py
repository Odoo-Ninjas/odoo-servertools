from odoo import api, SUPERUSER_ID
import traceback
import odoo
from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Configuration(models.Model):
    _name = "mousetrap.configuration"

    name = fields.Char("Name")
    code = fields.Text("Code", required=True)
    do_raise = fields.Boolean("Do Raise", default=True)

    method_trigger_ids = fields.One2many(
        "mousetrap.hook", "config_id", string="Triggers"
    )

    def _trigger(self, instances, args_packed, method):
        self._start_by_methodhook(instances, args_packed, method)

    def _start_by_methodhook(self, records, args, method):
        for record in records:
            objects = {
                "record": record,
            }
            do_raise = self.do_raise
            try:
                res = self._exec_get_result(self.code, objects)
                if not res:
                    raise Exception(f"Condition is false: {self.code}")
            except Exception as ex:

                trace = "\n".join(traceback.format_stack())
                breakpoint()

                with odoo.api.Environment.manage():
                    with odoo.registry(self.env.cr.dbname).cursor() as new_cr:
                        new_cr.execute(
                            (
                                "insert into mousetrap_catches(create_date, excinfo, stacktrace) "
                                "values(%s, %s, %s)"
                            ),
                            (fields.Datetime.now(), str(ex), trace),
                        )
                        new_cr.commit()

                if do_raise:
                    raise

    @api.model
    def _exec_get_result(self, code, globals_dict):
        if not code:
            raise ValidationError("Code missing")
        from copy import deepcopy

        dict2 = {k: v for (k, v) in globals_dict.items()}
        del globals_dict

        dict2["env"] = self.env

        code = (code or "").strip()
        code = code.splitlines()
        if code and code[-1].startswith(" ") or code[-1].startswith("\t"):
            code.append("True")
        code[-1] = (
            "return " + code[-1] if not code[-1].startswith("return ") else code[-1]
        )
        code = "\n".join(["  " + x for x in code])
        keys = ",".join(list(dict2.keys()))
        wrapper = (
            f"def __wrap({keys}):\n"
            f"{code}\n\n"
            f"result_dict['result'] = __wrap({keys})"
        )
        result_dict = {}
        dict2["result_dict"] = result_dict
        exec(wrapper, dict2)
        return result_dict.get("result")
