package com.homelessqrypto.homelessqryptoapp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class QRHistoryPage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_qrhistory_page);

        Intent intent = getIntent();
        String idMessage = intent.getStringExtra("id");
        String qrMessage = intent.getStringExtra("qr");

        if (idMessage != null) {

        } else if (qrMessage != null) {

        }
    }
}
