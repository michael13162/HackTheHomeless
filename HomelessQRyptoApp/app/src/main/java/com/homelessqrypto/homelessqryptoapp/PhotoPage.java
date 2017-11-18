package com.homelessqrypto.homelessqryptoapp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.Result;

import me.dm7.barcodescanner.zxing.ZXingScannerView;

public class PhotoPage extends AppCompatActivity implements ZXingScannerView.ResultHandler {
    private ZXingScannerView mScannerView;

    int target;

    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);
        mScannerView = new ZXingScannerView(this);   // Programmatically initialize the scanner view
        setContentView(mScannerView);
        target = getIntent().getIntExtra(MainPage.TARGET, MainPage.QR_HISTORY_PAGE);
    }

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
        if(rawResult.getBarcodeFormat() == BarcodeFormat.QR_CODE) {
            if(target == MainPage.QR_HISTORY_PAGE){
                Intent intent = new Intent(this, QRHistoryPage.class);
                intent.putExtra(MainPage.QR_STRING, rawResult.getText());    // send this to the activity it is needed in
                startActivity(intent);
            }
            else { // target == SALE_PAGE

            }
        }
        else {
            // need to send message and
            //try again
            mScannerView.resumeCameraPreview(this);
        }
    }
}
