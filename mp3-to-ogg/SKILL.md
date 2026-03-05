---
name: mp3-to-ogg
description: Converte arquivos de áudio MP3 para OGG, mantendo o nome do arquivo original e alterando apenas a extensão. Use quando precisar converter um arquivo MP3 para OGG para compatibilidade ou tamanho de arquivo. Este skill utiliza ffmpeg para a conversão.
---

# MP3 para OGG Converter

Este skill permite converter facilmente arquivos MP3 para o formato OGG, útil para compatibilidade com diferentes plataformas ou para otimização de tamanho de arquivo.

## Uso

Para converter um arquivo MP3 para OGG, use o script `convert_mp3_to_ogg.py` com o caminho do arquivo MP3 como argumento:

```bash
python scripts/convert_mp3_to_ogg.py <caminho_do_arquivo_mp3>
```

O arquivo OGG resultante será salvo no mesmo diretório do arquivo MP3 original, com o mesmo nome, mas com a extensão `.ogg`.

**Exemplo:**

Se você tiver um arquivo MP3 em `/home/opc/audio.mp3`, o comando irá gerar `/home/opc/audio.ogg`.
