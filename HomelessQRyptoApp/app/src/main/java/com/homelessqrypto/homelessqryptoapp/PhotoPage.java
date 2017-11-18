package com.homelessqrypto.homelessqryptoapp;

import android.app.AlertDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.content.Intent;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.Result;


import me.dm7.barcodescanner.zxing.ZXingScannerView;

public class PhotoPage extends AppCompatActivity implements ZXingScannerView.ResultHandler{


    private ZXingScannerView mScannerView;

    int target;

    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);
        mScannerView = new ZXingScannerView(this);   // Programmatically initialize the scanner view
        target = getIntent().getIntExtra(MainPage.TARGET, MainPage.QR_HISTORY_PAGE);
        mScannerView.setAutoFocus(true);
//        IntentIntegrator integrator = new IntentIntegrator(this);
//        integrator.initiateScan(IntentIntegrator.QR_CODE_TYPES);
        setContentView(mScannerView);
    }
/*
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);
        Snackbar.make(findViewById(this.getTaskId()), scanResult.getFormatName(),
                Snackbar.LENGTH_SHORT)
                .show();
        if (scanResult != null) {
            // handle scan result
            if(scanResult.getFormatName() == "QR_CODE") {
                Intent newIntent = new Intent(this, QRHistoryPage.class);
                newIntent.putExtra(MainPage.QR_STRING, scanResult.getContents());
                startActivity(newIntent);
            }
            else{
                Snackbar.make(findViewById(this.getTaskId()), scanResult.getFormatName(),
                        Snackbar.LENGTH_SHORT)
                        .show();
            }
        }
        // else continue with any other code you need in the method

    }*/

    @Override
    public void onResume() {
        super.onResume();
        mScannerView.setResultHandler(this); // Register ourselves as a handler for scan results.
        mScannerView.startCamera();          // Start camera on resume
    }

    @Override
    public void onPause() {
        super.onPause();
        mScannerView.stopCamera();           // Stop camera on pause
    }

    @Override
    public void handleResult(Result rawResult) {
        // Do something with the result here

//        Log.e("TEXT: ", rawResult.getText()); // Prints scan results<br />
//        Log.e("TYPE: ", rawResult.getBarcodeFormat().toString());// Prints the scan format (qrcode)</p>
//        AlertDialog.Builder builder = new AlertDialog.Builder(this);
//        builder.setTitle("Result");
//        builder.setMessage(rawResult.getText());
//        AlertDialog alert1 = builder.create();
//        alert1.show();

        if(rawResult != null && rawResult.getBarcodeFormat() == BarcodeFormat.QR_CODE) {
            if(target == MainPage.QR_HISTORY_PAGE){
                Intent intent = new Intent(this, QRHistoryPage.class);
                intent.putExtra("qr", rawResult.getText());    // send this to the activity it is needed in
                startActivity(intent);
            }
            else { // target == SALE_PAGE
                Intent intent = new Intent(this, SalePage.class);
                intent.putExtra("qr", rawResult.getText());    // send this to the activity it is needed in
                startActivity(intent);
            }
        }
        else {
            // need to send message and
            //try again
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("");
            builder.setMessage("Please center the QR code in the box and allow it to be captured");
            AlertDialog alert1 = builder.create();
            alert1.show();
            mScannerView.resumeCameraPreview(this);
        }
    }




}
