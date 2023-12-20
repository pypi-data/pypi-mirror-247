from setuptools import setup, find_packages

setup(
    name='azucar_reactive_websocket',
    version='0.2.1',
    author='juan_k704',
    author_email='juan_k704@hotmail.com',
    description='Un manejador de WebSocket reactivo usando RxPython y websockets.',
    packages=find_packages(),
    install_requires=[
        'rx',          # RxPython para programación reactiva
        'websockets'   # Biblioteca para trabajar con WebSockets
    ],
    classifiers=[
        # Indica a quién va dirigido tu paquete y en qué etapas de desarrollo se encuentra
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Versión mínima de Python requerida
)
