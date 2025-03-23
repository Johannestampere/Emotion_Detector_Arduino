int happy = 13;
int sad = 12; 
int angry = 11;
int fear = 10;
int neutral = 9;

void setup() {
    pinMode(happy, OUTPUT);
    pinMode(sad, OUTPUT);
    pinMode(angry, OUTPUT);
    pinMode(fear, OUTPUT);
    pinMode(neutral, OUTPUT);

    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        char emotion = Serial.read();

        digitalWrite(happy, LOW);
        digitalWrite(sad, LOW);
        digitalWrite(angry, LOW);
        digitalWrite(neutral, LOW);
        digitalWrite(fear, LOW);

        if (emotion == 'h') {
            digitalWrite(happy, HIGH);
        } else if (emotion == 's') {
            digitalWrite(sad, HIGH);
        } else if (emotion == 'a') {
            digitalWrite(angry, HIGH);
        } else if (emotion == 'f') {
            digitalWrite(fear, HIGH);
        } else if (emotion == 'n') {
            digitalWrite(neutral, HIGH);
        } else if (emotion == '0') {
          
        } else {
            Serial.println("unknown char");
        }
    }
}