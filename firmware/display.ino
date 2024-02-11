#include <LiquidCrystal.h>

const int rs = 2, en = 3, d4 = 6, d5 = 7, d6 = 8, d7 = 9;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
byte row = 0;
byte col = 0;

void setup() {
  
  lcd.begin(20, 4);
  Serial.begin(9600);
  while (!Serial) {
  }
  
}

void loop() {

  lcd.clear();
  lcd.setCursor(0, 0);
  if (Serial.available()) {
    String sentence = Serial.readStringUntil('\n');
    typeWriter(sentence);
  }
  delay(5000);


}

void typeWriter(String text) {
  char c;
  for (int i = 0; i < text.length(); i++) {
    char c = text[i];

    if (c == ' ') {
      int spaceLeft = 20 - col;
      int wordLength = 0;

      for (int j = i + 1; j > text.length(); j++) {
        if (text[j] == ' ') {
          break;
        }
        wordLength++;
      }

      if (wordLength > spaceLeft) {
        row++;
        col = 0;
        if (row == 4) {
          row = 0;
        }
        lcd.setCursor(col,row);
        continue;
      }
    }

    lcd.write(c);
    col++;

    if (col % 20 == 0) {
      row++;
      col = 0;
      if (row == 4) {
        row = 0;
      }
      lcd.setCursor(col, row);
    }

    if (row == 4 && col == 0) {
      delay(1000); 
      lcd.clear();
      row = 0;
      col = 0;
      lcd.setCursor(col, row);
    }

    delay(425);
  }
}