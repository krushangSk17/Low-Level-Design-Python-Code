class Package:
    def __init__(self, name):
        self.name = name
        self.dependencies = []

    def install(self, manager, currently_installing=None):
        if not manager.is_installed(self.name):
            if currently_installing is None:
                currently_installing = set()

            if self.name in currently_installing:
                raise Exception(f"Cyclic dependency detected at {self.name}. Installation aborted.")

            currently_installing.add(self.name)

            for dependency in self.dependencies:
                dependency.install(manager, currently_installing)

            currently_installing.remove(self.name)
            print(f"Installing {self.name}")
            manager.mark_as_installed(self.name)

class PackageManager:
    def __init__(self):
        self.installed_packages = set()

    def install_package(self, package):
        try:
            package.install(self)
        except Exception as e:
            print(e)

    def is_installed(self, name):
        return name in self.installed_packages

    def mark_as_installed(self, name):
        self.installed_packages.add(name)

    def add_package(self, name, dependencies):
        package = Package(name)
        package.dependencies = dependencies
        return package

def main():
    manager = PackageManager()

    # Create packages with dependencies
    packageA = Package('A')
    packageB = Package('B')
    packageC = Package('C')
    packageD = Package('D')
    packageE = Package('E')
    packageF = Package('F')
    packageG = Package('G')

    # Setting dependencies
    packageA.dependencies = [packageB, packageC]
    packageB.dependencies = [packageD, packageE]
    packageC.dependencies = [packageF]
    packageF.dependencies = [packageG]
    # packageG.dependencies = [packageA]  # Introduces a cycle intentionally

    # Test installing a package with a cycle
    print("Installing package A (with cyclic dependency):")
    manager.install_package(packageA)
    print()

    # Test installing a package with no dependencies
    print("Installing package D (no dependencies):")
    manager.install_package(packageD)
    print()

    # Test reinstallation of an already installed package
    print("Reinstalling package A:")
    manager.install_package(packageA)
    print()

if __name__ == "__main__":
    main()
