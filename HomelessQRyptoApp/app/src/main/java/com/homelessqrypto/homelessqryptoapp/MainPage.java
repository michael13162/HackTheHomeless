package com.homelessqrypto.homelessqryptoapp;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.ContactsContract;
import android.provider.MediaStore;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.UUID;

public class MainPage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_page);

        File file = new File(this.getFilesDir(), "user_info.txt");
        if (file.exists() && file.canRead()) {
            try {
                BufferedReader reader = new BufferedReader(new FileReader(file));
                GlobalApplicationProperties.name = reader.readLine();
                GlobalApplicationProperties.email = reader.readLine();
                GlobalApplicationProperties.password = reader.readLine();
            } catch (Exception e) { }
        } else {
            try {
                FileWriter writer = new FileWriter(file);
                Cursor c = getApplication().getContentResolver().query(ContactsContract.Profile.CONTENT_URI, null, null, null, null);
                c.moveToFirst();
                String name = c.getString(c.getColumnIndex("display_name"));
                c.close();
                GlobalApplicationProperties.name = name;
                GlobalApplicationProperties.email = name + "@gmail.com";
                GlobalApplicationProperties.password = UUID.randomUUID().toString();
                writer.write(GlobalApplicationProperties.name);
                writer.write(GlobalApplicationProperties.email);
                writer.write(GlobalApplicationProperties.password);
            } catch (Exception e) { }
        }
    }

    ////////////////////////////////////////////////////////////////////////////

    public void toPurchase(View view) {
        // make the Purchase page what is shown
        Intent intent = new Intent(this, PurchasePage.class);
        startActivity(intent);
    }

    public void toTakeDonate(View view) {
        // just go to camera
//        allowTakePhoto();
        // if just to camera, have a message about good photo
        // While processing the image, which screen to go to?
        // if fail, request user try again in a message, screen back to camera
    }

    static final int SINGLE_IMAGE_REQUEST = 1;
/*
    private void allowTakePhoto() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        // Ensure that there's a camera activity to handle the intent
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            // Create the File where the photo should go
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                // Error occurred while creating the File
         // Give message box  -- unable to take picture at this time
            }
            // Continue only if the File was successfully created
            if (photoFile != null) {
                Uri photoURI = FileProvider.getUriForFile(this,
                        "com.example.android.fileprovider",
                        photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePictureIntent, SINGLE_IMAGE_REQUEST);
            }
        }
    }
*/
    // gets the images and attempts to decode the QR code
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == SINGLE_IMAGE_REQUEST && resultCode == RESULT_OK) {
            // get image data, attempt decode on success, change view

            // The new image should be at this location




            File file = new File(photoPath);
            if (file != null) {
                file.delete();
            }
            // else TRY AGAIN
        }
    }

    String PHOTONAME = "QRcodeImage";
    String photoPath;

    private File createImageFile() throws IOException {
        // Create an image file
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                PHOTONAME,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        photoPath = image.getAbsolutePath();
        return image;
    }

    public void toDonateHistory(View view) {
        // make the Donation History page what is shown
        Intent intent = new Intent(this, DonationHistoryPage.class);
        startActivity(intent);
    }
}
