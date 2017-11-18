package com.homelessqrypto.homelessqryptoapp;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class QRHistoryPage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_qrhistory_page);

        Intent intent = getIntent();
        String idMessage = intent.getStringExtra("id");
        String qrMessage = intent.getStringExtra("qr");

        final RequestQueue queue = Volley.newRequestQueue(this);
        final Context me = this;

        try {
            String url = GlobalApplicationProperties.serverUrl + "/api/account/user/purchases?";
            if (idMessage != null) {
                url += "spenderId=" + idMessage;
            } else if (qrMessage != null) {
                url += "publicHash=" + idMessage;
            }
            JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                JSONArray purchases = response.getJSONArray("purchases");
                                int homelessId = 0;
                                for (int i = 0; i < purchases.length(); i++) {
                                    final JSONObject purchase = purchases.getJSONObject(i);
                                    homelessId = (Integer) purchase.get("id");

                                    LinearLayout purchaseHistoryLayout = (LinearLayout) findViewById(R.id.purchase_history_layout);
                                    LinearLayout addedLayout = new LinearLayout(me);
                                    addedLayout.setOrientation(LinearLayout.HORIZONTAL);
                                    LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
                                    addedLayout.setLayoutParams(layoutParams);

                                    TextView dateText = new TextView(me);
                                    dateText.setText(purchase.get("date").toString());
                                    dateText.setGravity(Gravity.CENTER);
                                    LinearLayout.LayoutParams dateLayoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
                                    dateText.setLayoutParams(dateLayoutParams);
                                    addedLayout.addView(dateText);

                                    TextView descriptionText = new TextView(me);
                                    descriptionText.setText(purchase.get("description").toString());
                                    descriptionText.setGravity(Gravity.CENTER);
                                    LinearLayout.LayoutParams descriptionLayoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
                                    descriptionText.setLayoutParams(descriptionLayoutParams);
                                    addedLayout.addView(descriptionText);

                                    TextView amountText = new TextView(me);
                                    amountText.setText(String.format("%.2f", (Double) purchase.get("amount")));
                                    amountText.setGravity(Gravity.CENTER);
                                    LinearLayout.LayoutParams amountLayoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
                                    amountText.setLayoutParams(amountLayoutParams);
                                    addedLayout.addView(amountText);

                                    purchaseHistoryLayout.addView(addedLayout);
                                }

                                String user_url = GlobalApplicationProperties.serverUrl + "/api/account/user/" + homelessId;

                                JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, user_url,
                                        new Response.Listener<JSONObject>() {
                                            @Override
                                            public void onResponse(JSONObject response) {
                                                try {
                                                    String name = response.get("name").toString();
                                                    String balance = String.format("%.2f", (Double) response.get("balance"));

                                                    TextView descriptionText = (TextView) findViewById(R.id.description_text);
                                                    descriptionText.setText(name + " - " + balance + " HTH");
                                                } catch (JSONException e) { }
                                            }
                                        },
                                        new Response.ErrorListener() {
                                            @Override
                                            public void onErrorResponse(VolleyError error) { }
                                        });

                                queue.add(request);
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

        Button donateButton = findViewById(R.id.donation_button);
        donateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                
            }
        });
    }
}
