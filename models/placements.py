from odoo import models, fields, api, _
import base64


class PlacementsForm(models.Model):
    _name = 'logic.placement.form'
    _description = 'Placement Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('logic.students', string='Student Name')
    batch_id = fields.Many2one('logic.base.batch', string='Batch', related='student_id.batch_id')
    course_id = fields.Many2one('logic.base.courses', string='Course', related='batch_id.course_id')
    company_name = fields.Char(string='Company Name')
    job_position = fields.Char(string='Job Position')
    starting_salary = fields.Float(string='Starting Salary')
    joining_date = fields.Date(string='Joining Date')
    created_date = fields.Date(string='Added Date', default=fields.Date.today, readonly=1)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    updated_photo = fields.Binary(string='Updated Photo')
    branch = fields.Many2one('logic.base.branches', related='batch_id.branch_id', string='Branch')
    download_photo = fields.Binary(string='Download Photo', compute='_compute_download_photo', store=True)
    experience_duration = fields.Float('Experience')
    exp_period = fields.Selection([('year', 'Year'), ('month', 'Month'), ('day', 'Day')], string='Duration',
                                  default='year')
    photo_bool = fields.Boolean('photo')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft', tracking=True)

    def _compute_display_name(self):
        for record in self:
            if record.student_id:
                record.display_name = record.student_id.name + '  ' + 'Placement Record'

    @api.depends('updated_photo')
    def _compute_download_photo(self):
        for record in self:
            if record.updated_photo:
                record.photo_bool = True
                record.download_photo = record.updated_photo
            else:
                record.photo_bool = False

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
