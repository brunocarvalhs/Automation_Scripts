import os
import re
import argparse
import unittest
import tempfile
import shutil
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GradleParser:
    def __init__(self, project_directory, replace):
        self.gradle_dependencies = {}
        self.gradle_plugins = {}
        self.gradle_bundles = {}
        self.project_directory = project_directory or "."
        self.replace = replace

        # Expressões regulares
        self.dependency_pattern = re.compile(r'(\w+)\(["\']([^:"\']+):([^:"\']+):([^:"\']+)')
        self.plugin_pattern = re.compile(r'apply[ \t]+plugin:[ \t]+["\']([^:"\']+):([^:"\']+)["\']')
        self.bundle_pattern = re.compile(r'bundle[ \t]+["\']([^:"\']+):([^:"\']+):([^:"\']+)')
        self.gradle_files = []

        # Configurações de dependência, plugin e bundle permitidas
        self.dependency_configurations = [
            'implementation',
            'testImplementation',
            'androidTestImplementation',
            'debugImplementation',
            'releaseImplementation',
            'kaptTest',
            'kapt',
            'testAnnotationProcessor',
        ]

    def parse(self):
        try:
            # Percorre recursivamente o diretório do projeto e faz o parsing dos arquivos Gradle
            for root, dirs, files in os.walk(self.project_directory):
                for file_name in files:
                    # Verifique se o arquivo é um build.gradle ou build.gradle.kts
                    if file_name in ('build.gradle', 'build.gradle.kts'):
                        file_path = os.path.join(root, file_name)
                        self.gradle_files.append(file_path)

            # Abre cada arquivo Gradle, encontra as dependências, plugins e bundles e adiciona-os às listas correspondentes
            for gradle_file in self.gradle_files:
                with open(gradle_file, 'r') as file:
                    content = file.read()

                    # Encontra dependências
                    for configuration in self.dependency_configurations:
                        pattern = re.compile(f'{configuration}\(["\']([^:"\']+):([^:"\']+):([^:"\']+)')
                        matches = pattern.findall(content)
                        for match in matches:
                            group, name, version = match
                            key = name.lower()  # Use o nome como chave única
                            if key not in self.gradle_dependencies:
                                self.gradle_dependencies[key] = {
                                    "group": group,
                                    "name": name,
                                    "version": version,
                                }

                    # Encontra plugins
                    plugin_matches = self.plugin_pattern.findall(content)
                    for match in plugin_matches:
                        plugin_group, plugin_name = match
                        plugin_key = f'{plugin_group}:{plugin_name}'
                        self.gradle_plugins[plugin_key] = {
                            "group": plugin_group,
                            "name": plugin_name,
                        }

                    # Encontra bundles
                    bundle_matches = self.bundle_pattern.findall(content)
                    for match in bundle_matches:
                        bundle_group, bundle_name, bundle_version = match
                        bundle_key = f'{bundle_group}:{bundle_name}'
                        self.gradle_bundles[bundle_key] = {
                            "group": bundle_group,
                            "name": bundle_name,
                            "version": bundle_version,
                        }

            logger.info("Parsing completed successfully.")
        except Exception as e:
            logger.error(f"Error during parsing: {str(e)}")

    def save_to_toml(self, output_file_path):
        try:
            # Salva as dependências, plugins e bundles em um arquivo TOML
            with open(output_file_path, 'w') as toml_file:
                toml_file.write("[versions]\n")
                for key, value in self.gradle_dependencies.items():
                    toml_file.write(f'{key} = "{value["version"]}"\n')

                toml_file.write("\n[libraries]\n")
                for key, value in self.gradle_dependencies.items():
                    toml_file.write(f'{key} = {{ group = "{value["group"]}", name = "{value["name"]}", version = "{key}" }}\n')

                toml_file.write("\n[plugins]\n")
                for key, value in self.gradle_plugins.items():
                    toml_file.write(f'{key} = {{ group = "{value["group"]}", name = "{value["name"]}" }}\n')

                toml_file.write("\n[bundles]\n")
                for key, value in self.gradle_bundles.items():
                    toml_file.write(f'{key} = {{ group = "{value["group"]}", name = "{value["name"]}", version = "{value["version"]}" }}\n')

            logger.info(f"Saved data to {output_file_path}.")
        except Exception as e:
            logger.error(f"Error while saving to TOML: {str(e)}")

    def replace_dependencies(self):
        try:
            # Processa os arquivos Gradle novamente para substituir as dependências
            for gradle_file in self.gradle_files:
                with open(gradle_file, 'r') as file:
                    content = file.read()
                    for key, value in self.gradle_dependencies.items():
                        dependency_string = f'\'{value["group"]}:{value["name"]}:{value["version"]}\''
                        if gradle_file.endswith('.gradle.kts'):
                            dependency_string = f'\"{value["group"]}:{value["name"]}:{value["version"]}\"'
                        replacement = f'libs.{key.replace("-", ".")}'
                        content = content.replace(dependency_string, replacement)

                # Substitui o conteúdo do arquivo original pelo conteúdo modificado
                with open(gradle_file, 'w') as file:
                    file.write(content)

            logger.info("Replaced dependencies successfully.")
        except Exception as e:
            logger.error(f"Error while replacing dependencies: {str(e)}")

class TestGradleParser(unittest.TestCase):
    def setUp(self):
        # Cria um diretório temporário e arquivos de exemplo para testar o parser
        self.temp_dir = tempfile.mkdtemp()
        self.project_directory = os.path.join(self.temp_dir, 'test_project')
        os.makedirs(self.project_directory)
        self.build_gradle_path = os.path.join(self.project_directory, 'build.gradle')
        self.build_gradle_content = """
        dependencies {
            implementation 'com.example:library:1.0'
            testImplementation 'junit:junit:4.12'
        }
        """
        with open(self.build_gradle_path, 'w') as build_gradle:
            build_gradle.write(self.build_gradle_content)

    def tearDown(self):
        # Limpa os diretórios e arquivos temporários após os testes
        shutil.rmtree(self.temp_dir)

    def test_parser(self):
        # Testa se o parser funciona corretamente
        gradle_parser = GradleParser(self.project_directory, replace=False)
        gradle_parser.parse()

        # Verifica se as dependências foram corretamente identificadas
        self.assertIn('library', gradle_parser.gradle_dependencies)
        self.assertEqual(gradle_parser.gradle_dependencies['library']['group'], 'com.example')
        self.assertEqual(gradle_parser.gradle_dependencies['library']['version'], '1.0')

        # Verifica se o plugin não foi identificado
        self.assertNotIn('junit', gradle_parser.gradle_plugins)

    def test_replace_dependencies(self):
        # Testa a substituição de dependências nos arquivos Gradle
        gradle_parser = GradleParser(self.project_directory, replace=True)
        gradle_parser.parse()

        # Verifica se a substituição ocorreu corretamente
        with open(self.build_gradle_path, 'r') as build_gradle:
            updated_content = build_gradle.read()
            self.assertNotIn('com.example:library:1.0', updated_content)
            self.assertIn('libs.library', updated_content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processa arquivos Gradle e cria um arquivo TOML com dependências, plugins e bundles.')
    parser.add_argument('project_directory', type=str, help='Caminho para o diretório do projeto')
    parser.add_argument('--replace', action='store_true', help='Substituir as dependências nos arquivos Gradle')
    args = parser.parse_args()

    gradle_parser = GradleParser(args.project_directory, args.replace)
    gradle_parser.parse()
    gradle_parser.save_to_toml(os.path.join(f'{args.project_directory}/gradle', 'libs.versions.toml'))

    if args.replace:
        gradle_parser.replace_dependencies()
