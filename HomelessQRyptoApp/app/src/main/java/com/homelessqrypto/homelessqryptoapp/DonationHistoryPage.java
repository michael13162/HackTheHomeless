package com.homelessqrypto.homelessqryptoapp;

import android.content.Context;
import android.content.Intent;
import android.graphics.drawable.GradientDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutCompat;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class DonationHistoryPage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_donation_history_page);

        final RequestQueue queue = Volley.newRequestQueue(this);
        final Context me = this;

        try {
            String url = GlobalApplicationProperties.serverUrl + "/api/account/user/donations";
            JSONObject jsonObject = new JSONObject("{\"email\":\"" + GlobalApplicationProperties.email + "\", \"password\":\"" + GlobalApplicationProperties.password + "\"}");
            JsonObjectRequest request = new JsonObjectRequest(url, jsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                JSONArray donations = response.getJSONArray("donations");
                                for (int i = 0; i < donations.length(); i++) {
                                    final JSONObject donation = donations.getJSONObject(i);
                                    LinearLayout donationHistoryLayout = (LinearLayout) findViewById(R.id.donation_history_layout);
                                    LinearLayout addedLayout = new LinearLayout(me);
                                    addedLayout.setOrientation(LinearLayout.HORIZONTAL);
                                    LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
                                    addedLayout.setLayoutParams(layoutParams);

                                    TextView dateText = new TextView(me);
                                    dateText.setText(donation.get("date").toString());
                                    dateText.setGravity(Gravity.CENTER);
                                    LinearLayout.LayoutParams dateLayoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
                                    dateText.setLayoutParams(dateLayoutParams);
                                    addedLayout.addView(dateText);

                                    TextView amountText = new TextView(me);
                                    amountText.setText(String.format("%.2f", (Double) donation.get("amount")));
                                    amountText.setGravity(Gravity.CENTER);
                                    LinearLayout.LayoutParams amountLayoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
                                    amountText.setLayoutParams(amountLayoutParams);
                                    addedLayout.addView(amountText);

                                    TextView nameText = new TextView(me);
                                    nameText.setText(donation.get("name").toString());
                                    nameText.setGravity(Gravity.CENTER);
                                    LinearLayout.LayoutParams nameLayoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
                                    nameText.setLayoutParams(nameLayoutParams);
                                    addedLayout.addView(nameText);

                                    Button seeMoreButton = new Button(me);
                                    seeMoreButton.setText("See More");
                                    seeMoreButton.setGravity(Gravity.CENTER);
                                    LinearLayout.LayoutParams buttonLayoutParams = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
                                    seeMoreButton.setLayoutParams(buttonLayoutParams);
                                    seeMoreButton.setOnClickListener(new View.OnClickListener() {
                                        @Override
                                        public void onClick(View view) {
                                            try {
                                                Intent intent = new Intent(me, QRHistoryPage.class);
                                                intent.putExtra("id", donation.get("id").toString());
                                                startActivity(intent);
                                            } catch (JSONException e) { }
                                        }
                                    });
                                    addedLayout.addView(seeMoreButton);

                                    donationHistoryLayout.addView(addedLayout);
                                }
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
    }
}
