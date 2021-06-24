package com.example.catchingcomputersapp;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.animation.AlphaAnimation;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {
    MainActivity instance = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        if (instance == null){instance = this;}
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button  = findViewById(R.id.main_activity_button);
        TextView busID = findViewById(R.id.text_bus_number);
        View loadingCircle = findViewById(R.id.loadingPanel);
        loadingCircle.setVisibility(View.GONE);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                button.setEnabled(false);
                button.setClickable(false);
                String id = busID.getText().toString();
                loadingCircle.setVisibility(View.VISIBLE);
                busID.setAlpha(0.2f);
                button.setAlpha(0.2f);
                if (isBusExists((id))) {
                    Intent i = new Intent(instance, picturesActivity.class);
                    i.putExtra("busID", id);
                    startActivity(i);

                }
//                Toast.makeText(instance, "Bus doesn't exist!", Toast.LENGTH_LONG).show();
                loadingCircle.setVisibility(View.GONE);
                busID.setAlpha(1f);
                button.setAlpha(1f);
                button.setEnabled(true);
                button.setClickable(true);
            }
        });
    }

    private boolean isBusExists(String id){
        return true; // TODO : IMPLEMENT
    }
}