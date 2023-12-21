The text colorizer everyone needs!
#
```python
import calar
```
# Example Usage
```python
calar.init() # Optional

blue_color = calar.get('blue')
# blue_color = calar.Fore.BLUE
# blue_color = calar.get('blue', 'fore')
print(blue_color + 'Hello World!')

calar.deinit() # Optional
```
# More Example Usage
```python
blended = calar.blend(calar.Fore.BLUE, calar.Style.BOLD)
print(blended + 'Hello World!')
```
# Create Gradients
```python
blue_gradient = calar.gradient('blue')
print(blue_gradient + 'Hello World!')

back_blue_gradient = calar.gradient('blue', 'back')
print(back_blue_gradient + 'Hello World!')
```

# Apply Gradients to Text
```python
gradient = calar.gradient('blue')
gradient_text = calar.gradientify('Hello World!', gradient)
print(gradient_text)
```

# Colorize Code
```python
code = '''
import numpy as np

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(5))
'''

colored_code = calar.code(code, 'python', 'friendly')
print(colored_code)
```