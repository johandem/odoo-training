from odoo import models, fields


class Task(models.Model):
    _name = 'coopplanning.task'

    name = fields.Char('Name')
    description = fields.Text('Description')
    nb_workers = fields.Integer('Nb Workers')
    task_type_id = fields.Many2one('coopplanning.task.type', string='Task Type')
    date_start = fields.Date('Start Date')
    completed = fileds.Boolean('Completed')
    
    task_id = fields.Many2one('coopplanning.task')
    worker_ids = fields.Many2many('coopplanning.volunteer')

class TaskType(models.Model):
    _name = 'coopplanning.task.type'

    name = fields.Char('Name')

class Assignment(models.Model):
    _name = 'coopplanning.assignment'

    task_id = fields.One2many('coopplanning.task')
    worker_id = fields.One2many('coopplanning.volunteer')