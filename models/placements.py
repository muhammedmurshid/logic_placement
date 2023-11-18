from odoo import models, fields, api, _


class PlacementsForm(models.Model):
    _name = 'logic.placement.form'
    _description = 'Placement Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('logic.students', string='Student Name')
    batch_id = fields.Many2one('logic.base.batch', string='Batch', related='student_id.batch_id')
    course_id = fields.Many2one('logic.base.courses', string='Course')
    company_name = fields.Char(string='Company Name')
    job_position = fields.Char(string='Job Position')
    starting_salary = fields.Float(string='Starting Salary')
    joining_date = fields.Date(string='Joining Date')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft', tracking=True)

    def _compute_display_name(self):
        for record in self:
            if record.student_id:
                record.display_name = record.student_id.name + '  ' + 'Placement Record'

    def action_done(self):
        student = self.env['logic.students'].browse(self.student_id.id)
        student.write({
            'placement_company_name': self.company_name,
            'placement_job_position': self.job_position,
            'placement_starting_salary': self.starting_salary,
            'placement_joining_date': self.joining_date
        })
        self.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Done',
                'type': 'rainbow_man',
            }
        }

    def action_draft(self):
        self.state = 'draft'
