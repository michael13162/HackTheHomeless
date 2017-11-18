package com.homelessqrypto.homelessqryptoapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class PurchasePage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_purchase_page);
        ImageView imageView = (ImageView) findViewById(R.id.logo_image);
        imageView.setImageResource(R.drawable.logo);

        final RequestQueue queue = Volley.newRequestQueue(this);

        try {
            String url = GlobalApplicationProperties.serverUrl + "/api/account/user";
            JSONObject jsonObject = new JSONObject("{\"email\":\"" + GlobalApplicationProperties.email + "\", \"password\":\"" + GlobalApplicationProperties.password + "\"}");
            JsonObjectRequest request = new JsonObjectRequest(url, jsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                double value = (Double) response.get("balance");
                                TextView balanceText = (TextView) findViewById(R.id.balance_text);
                                balanceText.setText("Balance: " + String.format("%.2f", value));
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

        Button freeCurrencyButton = findViewById(R.id.free_currency_button);
        freeCurrencyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    String url = GlobalApplicationProperties.serverUrl + "/api/account/user/buy";
                    JSONObject jsonObject = new JSONObject("{\"email\":\"" + GlobalApplicationProperties.email + "\", \"password\":\"" + GlobalApplicationProperties.password + "\", \"amount\":100}");
                    JsonObjectRequest request = new JsonObjectRequest(url, jsonObject,
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    TextView balanceText = (TextView) findViewById(R.id.balance_text);
                                    balanceText.setText("Balance: " + String.format("%.2f", Double.parseDouble(balanceText.getText().toString()) + 100));
                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                }
                            });
                    queue.add(request);
                } catch (JSONException e) { }
            }
        });
    }
}
