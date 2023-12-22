from kfp.v2 import dsl
from kfp.v2 import compiler
from google.cloud import aiplatform
class Experiment:
    def __init__(self, experiment_name, pipeline_root, path_template):
        self.experiment_name = experiment_name
        self.pipeline_root = pipeline_root
        self.path_template = path_template

    def compile_model(self, pipeline_func):
        @dsl.pipeline(name= f'componente-{self.experiment_name}')
        def pipeline(
                    params: dict, 
                    model_name: str
                    ):
            pipeline_func(params, model_name)

        compiler.Compiler().compile(pipeline_func=pipeline, package_path= self.path_template)

    def compile_hyperparameter(self, pipeline_func):

        @dsl.pipeline(name= f'componente-{self.experiment_name}')
        def pipeline(
                    params_dict: dict
                    ):
            pipeline_func(params_dict)

        compiler.Compiler().compile(pipeline_func=pipeline, package_path= self.path_template)

    def run_hyperparameter(self, runs):
        for i, run in enumerate(runs):
            job = aiplatform.PipelineJob(
                display_name=f"{self.experiment_name}-pipeline-run-{i}",
                template_path=self.path_template,
                pipeline_root=self.pipeline_root,
                parameter_values={"params_dict": run}
            )
            EXPERIMENT_NAME = self.experiment_name
            job.submit(experiment= EXPERIMENT_NAME)

    def run_model(self, runs):
        EXPERIMENT_NAME = self.experiment_name
        for i, run in enumerate(runs):
            job = aiplatform.PipelineJob(
                display_name=f"{self.experiment_name}-pipeline-run-{i}",
                template_path= self.path_template,
                pipeline_root=self.pipeline_root,
                parameter_values= {
                                    "params": run,
                                    "model_name": run["model_name"]
                                }
            )            
            job.submit(experiment= EXPERIMENT_NAME)
