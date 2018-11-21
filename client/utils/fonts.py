from tkinter import font

def _getFont(fontClass):
  fonts = {
    'title': font.Font(family='Press Start 2P', size=24),
    'title2': font.Font(family='Press Start 2P', size=16),
    'title3': font.Font(family='Press Start 2P', size=12),
    'body': font.Font(family='Silom', size=12),
  }

  return fonts[fontClass]
