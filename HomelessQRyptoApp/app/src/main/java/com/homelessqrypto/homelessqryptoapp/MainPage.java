package com.homelessqrypto.homelessqryptoapp;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.ContactsContract;
import android.provider.MediaStore;
import android.provider.Settings;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.UUID;



public class MainPage extends AppCompatActivity {

    public static final int QR_HISTORY_PAGE = 0;
    public static final int SALE_PAGE = 1;
    public static final String QR_STRING = "QR_string";
    public static final String TARGET = "target";

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

                RequestQueue queue = Volley.newRequestQueue(this);
                String url = GlobalApplicationProperties.serverUrl + "/api/account/register";
                JSONObject jsonObject = new JSONObject("{\"name\":\"" + GlobalApplicationProperties.name + "\", \"email\":\"" + GlobalApplicationProperties.email + "\", \"password\":\"" + GlobalApplicationProperties.password +"\"}");
                JsonObjectRequest request = new JsonObjectRequest(url, jsonObject,
                        new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject response) {
                            }
                        },
                        new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                            }
                        });
                queue.add(request);
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
        // if just to camera, have a message about good photo
        // While processing the image, which screen to go to?
        // if fail, request user try again in a message, screen back to camera

        Intent intent = new Intent(this, PhotoPage.class);
        intent.putExtra(TARGET, QR_HISTORY_PAGE);
        startActivity(intent);
    }

    public void toSell(View view) {
        Intent intent = new Intent(this, PhotoPage.class);
        intent.putExtra(TARGET, SALE_PAGE);
        startActivity(intent);
    }

    public void toDonateHistory(View view) {
        // make the Donation History page what is shown
        Intent intent = new Intent(this, DonationHistoryPage.class);
        startActivity(intent);
    }
}
