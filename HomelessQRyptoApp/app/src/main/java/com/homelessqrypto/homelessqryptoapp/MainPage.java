package com.homelessqrypto.homelessqryptoapp;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;

import java.io.File;
import java.io.IOException;


public class MainPage extends AppCompatActivity {

    public static final int QR_HISTORY_PAGE = 0;
    public static final int SALE_PAGE = 1;
    public static final String QR_STRING = "QR_string";
    public static final String TARGET = "target";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_page);
    }

    ////////////////////////////////////////////////////////////////////////////

    public void toPurchase(View view) {
        // make the Purchase page what is shown
        Intent intent = new Intent(this, PurchasePage.class);
        startActivity(intent);
    }

    public void toTakeDonate(View view) {
        // just go to camera
        // if just to camera, have a message about good photo
        // While processing the image, which screen to go to?
        // if fail, request user try again in a message, screen back to camera

        Intent intent = new Intent(this, PhotoPage.class);
        intent.putExtra(TARGET, QR_HISTORY_PAGE);
        startActivity(intent);
    }

    // gets the images and attempts to decode the QR code
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
            // get image data, attempt decode on success, change view

            // The new image should be at this location

            // else TRY AGAIN

    }

    public void toDonateHistory(View view) {
        // make the Donation History page what is shown
        Intent intent = new Intent(this, DonationHistoryPage.class);
        startActivity(intent);
    }
}
