package com.homelessqrypto.homelessqryptoapp;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class SalePage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sale_page);

        Intent intent = getIntent();
        final String qrMessage = intent.getStringExtra("qr");

        final RequestQueue queue = Volley.newRequestQueue(this);
        final Context me = this;

        try {
            String url = GlobalApplicationProperties.serverUrl + "/api/account/user/balance?publicHash=" + qrMessage;

            JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                String balance = response.get("balance").toString();
                                TextView balanceText = findViewById(R.id.textView6);
                                balanceText.setText(String.format("%.2f", Double.valueOf(balance)) + " HTH");
                            } catch (JSONException e) { }
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                        }
                    });
            queue.add(request);
        } catch (Exception e) { }

        Button sellButton = findViewById(R.id.sell_button);
        sellButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    String url = GlobalApplicationProperties.serverUrl + "/api/account/user/purchase";
                    EditText amountText = findViewById(R.id.editText2);
                    final Double amount = Double.parseDouble(amountText.getText().toString());

                    EditText descriptionText = findViewById(R.id.editText3);
                    String description = descriptionText.getText().toString();

                    JSONObject jsonObject = new JSONObject("{\"amount\":" + amount + ",\"description\":\"" + description + "\",\"email\":\"" + GlobalApplicationProperties.email + "\", \"password\":\"" + GlobalApplicationProperties.password + "\",\"publicHash\":\"" + qrMessage + "\"}");
                    Log.e("asd", url);
                    Log.e("qfe", jsonObject.toString());
                    JsonObjectRequest request = new JsonObjectRequest(url, jsonObject,
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    AlertDialog.Builder builder;
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                                        builder = new AlertDialog.Builder(me, android.R.style.Theme_Material_Dialog_Alert);
                                    } else {
                                        builder = new AlertDialog.Builder(me);
                                    }
                                    builder.setTitle("Purchase Succeeded")
                                            .setMessage("You received " + amount + " HTH")
                                            .setNeutralButton(android.R.string.ok, new DialogInterface.OnClickListener() {
                                                public void onClick(DialogInterface dialog, int which) {
                                                    Intent intent = new Intent(me, MainPage.class);
                                                    startActivity(intent);
                                                }
                                            })
                                            .setIcon(android.R.drawable.ic_dialog_alert)
                                            .show();
                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    AlertDialog.Builder builder;
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                                        builder = new AlertDialog.Builder(me, android.R.style.Theme_Material_Dialog_Alert);
                                    } else {
                                        builder = new AlertDialog.Builder(me);
                                    }
                                    builder.setTitle("Purchase Failed")
                                            .setMessage("Insufficient Funds to Make Purchase")
                                            .setNeutralButton(android.R.string.ok, new DialogInterface.OnClickListener() {
                                                public void onClick(DialogInterface dialog, int which) { }
                                            })
                                            .setIcon(android.R.drawable.ic_dialog_alert)
                                            .show();
                                }
                            });
                    queue.add(request);
                } catch (Exception e) { }
            }
        });
    }
}
