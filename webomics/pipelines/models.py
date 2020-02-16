""" What does models.CASCASE do?
    Need to look at more Nextflow examples, they might be able to have end
    script after last process, also tag in processes.
    Need to read API"""
from django.db import models


class Pipeline(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    def processes(self):
        # idk if we can easily access process here through iteration
        query = ProcessPipelineJoin.objects.values("process")
        query = query.filter(pipeline_id=self.id)
        return query

    def params(self):
        return ParamsChannel.objects.filter(pipeline_id=self.id)

    def render(self, stitch):
        # maybe write this to file?
        result = '#!/usr/bin/env nextflow\n' + '// ' + self.description + '\n'
        for param in self.params():
            result += param.render() + '\n'
        processes = self.processes()
        if stitch is None:
            stitch = [None for _ in range(processes.count())]
        # Need to check stitch zips correctly if given? ie same length
        for s, process in zip(stitch, self.processes()):
            result += process.render(s) + '\n'
        return result + '\n'


class Process(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    script = models.TextField()
    tag = models.TextField()

    def __str__(self):
        return self.name

    def inputs(self):
        return InOutputs.objects.filter(is_input=True, process_id=self.id)

    def outputs(self):
        return InOutputs.objects.filter(is_input=False, process_id=self.id)

    def render(self, stitch=None):
        """ Takes a process and renders it into Nextflow format."""
        result = '// ' + self.description + '\n'
        result += 'process ' + self.name + ' {\n'
        result += '\tinput:\n'
        inputs = self.inputs()
        if stitch is None:
            # Allowing no stitches as an option, to get process template
            # won't work in a pipeline
            stitch = [None for _ in range(inputs.count())]
        # Need to check stitch zips correctly if given? ie same length
        for s, input in zip(stitch, inputs):
            result += '\t' + input.render(s) + '\n'
        result += '\n\toutput:\n'
        for output in self.outputs():
            result += '\t' + output.render() + '\n'
        result += '\n\t"""\n\t' + self.script + '\n\t"""\n}'
        return result


class ProcessPipelineJoin(models.Model):
    """ Join table for Process and Pipeline, not using ManyToManyField as Need
        to preserve order when rendering a form"""
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']
        unique_together = (("process_id", "pipeline_id", "order"),)

    def __str__(self):
        return "%d %d %d" % (self.process_id, self.pipeline_id, self.order)


class InOutputs(models.Model):
    is_input = models.BooleanField()
    name = models.CharField(max_length=100)
    function = models.TextField()
    description = models.TextFielqd()
    process = models.ForeignKey(Process, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def render(self, stitch=None):
        """ Renders the in/output as text for nextflow pipeline files.
            Input names must be a reference to process output or processed
            parameter (file or channel etc). These are replaced when processes
            and therefore in/outputs are stitched together."""
        if stitch is None:
            stitch = self.name
        if self.is_input:
            return self.function + ' from ' + stitch
        return self.function + ' into ' + self.name


class ParamsChannel(models.Model):
    """ I dont like this implementation, maybe want multiple files or channels.
    """
    name = models.CharField(mex_length=200)
    function = models.TextField()
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def render(self):
        # I dont know what this should actually look like
        return self.function
