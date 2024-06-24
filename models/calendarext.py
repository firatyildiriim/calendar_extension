from odoo.exceptions import UserError
from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    calendar_event_id = fields.Many2one('calendar.event', string='Calendar Source', readonly=True)
    hours_spent = fields.Float(string='Hours Spent')
    description = fields.Html('Notes', readonly=True)



from odoo import api, models

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    project_id = fields.Many2one('project.project', string='Proje')
    stage_id = fields.Many2one('project.stage', string='Aşama')






    def create_project_action(self):
        print("....context", self.env.context)
        Project = self.env['project.project']
        project_vals = {
            'name': self.name,
            'description': self.description,

        }
        project = Project.create(project_vals)

        return True

    def action_create_my_task(self):
        print(self.env.context)
        print("....context", self.env.context)
        Task = self.env['project.task']
        project_task = {
            'name': self.name,
            'calendar_event_id': self.id,
            'hours_spent': self.duration,

        }
        task = Task.create(project_task)

        return True

    def action_add_attendee(self):
        task = self.env['project.task'].search([('calendar_event_id', '=', self.id)], limit=1)

        partner_info_list = []
        for partner in self.partner_ids:
            partner_info = f" İsim: {partner.name} Mail: {partner.email} Telefon: {partner.phone} "
            partner_info_list.append(partner_info)

        html_partner_info = "<p><strong>Katılımcılar:</strong></p><ul>"
        for partner_info in partner_info_list:
            html_partner_info += f"<li>{partner_info}</li>"
        html_partner_info += "</ul>"

        task.write({'description': html_partner_info})

    def action_create_task(self):
        if not self.project_id:
            raise UserError("Proje seçilmediği için görev oluşturulamadı. Lütfen bir proje seçiniz.")


        Task = self.env['project.task']
        new_task = Task.create({
            'name': self.name,
            'hours_spent': self.duration,
            'calendar_event_id': self.id,
            'project_id': self.project_id.id,
        })

        return True

""" def action_create_subtask(self):
        from . import project_task

        if not self.project_id:
            raise UserError("Proje seçilmediği için alt görev oluşturulamadı. Lütfen bir proje seçiniz.")

        calendar_event_id = self.id
        project_task_id = self.task_id


        participants = self.attendee_ids


        for participant in participants:
            subtask_vals = {
                'name': participant.name,
                'project_id': project_task_id,
            }
            project_task.create(subtask_vals)


        return True

    def _generate_attendee_info(self):
        # Katılımcı bilgilerini topla ve HTML formatına dönüştür
        partner_info_list = []
        for partner in self.partner_ids:
            partner_info = f" İsim: {partner.name} Mail: {partner.email} Telefon: {partner.phone})"
            partner_info_list.append(partner_info)

        html_partner_info = "<p><strong>Katılımcılar:</strong></p><ul>"
        for partner_info in partner_info_list:
            html_partner_info += f"<li>{partner_info}</li>"
        html_partner_info += "</ul>"
        

        return html_partner_info
    """















