
from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    calendar_event_id = fields.Many2one('calendar.event', string='Calendar Source', readonly=True)
    hours_spent = fields.Float(string='Hours Spent')
    katilimci_ad = fields.Many2one('calendar.event', string='Attendance Name')
    katilimci_mail = fields.Many2one('calendar.event', string='Attendance Mail')
    note = fields.Html('Notes', readonly=True)



from odoo import api, models

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    project_id = fields.Many2one('project.project', string='Proje')
    participant_id = fields.Many2one('project.project', string='Proje')





    def create_project_action(self):
        # Burada proje oluşturma işlemini gerçekleştirecek kodu ekleyin
        # Örneğin:
        print("....context", self.env.context)
        Project = self.env['project.project']
        project_vals = {
            'name': self.name,  # veya istediğiniz proje adı
            'description': self.description,  # veya istediğiniz proje açıklaması
            # Diğer gerekli alanlar
        }
        project = Project.create(project_vals)
        # Proje oluşturulduktan sonra gerekli işlemleri yapabilirsiniz
        return True

    def action_create_my_task(self):
        print(self.env.context)
        print("....context", self.env.context)
        Task = self.env['project.task']
        project_task = {
            'name': self.name, # veya istediğiniz proje adı
            'calendar_event_id': self.id,
            'hours_spent': self.duration,
            # Diğer gerekli alanlar
        }
        task = Task.create(project_task)
         # Proje oluşturulduktan sonra gerekli işlemleri yapabilirsiniz
        return True

    def action_add_attendee(self):
        task = self.env['project.task'].search([('calendar_event_id', '=', self.id)], limit=1)

        partner_info_list = []
        for partner in self.partner_ids:
            partner_info = f" İsim: {partner.name} Mail: {partner.email} Telefon: {partner.phone})"
            partner_info_list.append(partner_info)

        html_partner_info = "<p><strong>Katılımcılar:</strong></p><ul>"
        for partner_info in partner_info_list:
            html_partner_info += f"<li>{partner_info}</li>"
        html_partner_info += "</ul>"

        task.write({'description': html_partner_info})

    def action_create_task(self):
        for event in self:
            if event.project_id:
                Task = self.env['project.task']
                new_task = Task.create({
                    'name': self.name,  # Görevin adı buraya gelebilir
                    'hours_spent': self.duration,
                    'calendar_event_id': self.id,
                    'project_id': event.project_id.id,
                    # İhtiyaca göre diğer alanlar da eklenebilir
                })
        return True
















