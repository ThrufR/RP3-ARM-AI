# Silnik rozpoznawania tekstu
##Założenia

W projekcie silnik rozpoznawania tekstu jest odpowiedzialny za poprawne wykrycie i rozpoznanie tekstu, który mamy na klockach.

Zakładamy, że strona sprzętowa wysyła nam sygnał startujący nasz program.
Z kolei nasz program może zwracać stronie sprzętowej miejsca, w których tekst został wykryty oraz jego treść.

Dzięki temu (w zależności od treści) program będzie mógł prawidłowo zareagować - ułożyć klocki w pożądanej pozycji.

##Do uruchomienia potrzebne będzie

Silnik zaprojektowany został w OpenCV z Python bindings.

Poza tym oprogramowaniem konieczne będą następujące biblioteki (plik requirements.txt). Instalujemy je w stworzonym przez nas środowisku wirtualnym.

Niezbędny jest również plik frozen_east_text_detection.pb.

##Działanie programu 

Korzystając z EAST Text Detectora (EAST: An Efficient and Accurate Scene Text Detector) możemy dokonywać detekcji oraz rozpoznawania tekstu.
Próbowaliśmy korzystać również z PyTesseract, ale algorytm nie posiadał takiej dokładności.
Znacznie gorzej również rozpoznaje fonty.

Algorytm przetwarza zdjęcie "od góry do dołu" w osi Y, i "od lewej do prawej" w osi X.

Użytym przez nas fontem dla nadruku na klockach był Arial. Sprawdziła się tutaj zasada "im prostszy font tym lepszy" - rozpoznawanie np. ręcznie napisanego wyrazu, z pozoru starannie, było niemożliwe.

##Źródła
1. https://arxiv.org/pdf/1704.03155.pdf
2. https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/
3. https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
4. https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html
5. https://realpython.com/python-virtual-environments-a-primer/
6. https://github.com/madmaze/pytesseract
7. https://stackabuse.com/pytesseract-simple-python-optical-character-recognition/
8. https://towardsdatascience.com/a-gentle-introduction-to-ocr-ee1469a201aa
9. https://medium.com/@eltronicsvilla17/text-recognition-7286606e57ba