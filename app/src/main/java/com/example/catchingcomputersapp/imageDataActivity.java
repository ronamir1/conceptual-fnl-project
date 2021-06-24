package com.example.catchingcomputersapp;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.imageview.ShapeableImageView;

import java.io.Serializable;

import uk.co.senab.photoview.PhotoViewAttacher;

public class imageDataActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_data);
        TextView text = findViewById(R.id.image_data_date_created);
        ShapeableImageView imageView = findViewById(R.id.image_data_imageToShow);
        Bitmap bm = BitmapFactory.decodeByteArray(getIntent().getByteArrayExtra("byteArray"),0,getIntent().getByteArrayExtra("byteArray").length);
        imageView.setImageBitmap(bm);

        PhotoViewAttacher pAttacher;
        pAttacher = new PhotoViewAttacher(imageView);
        pAttacher.update();

        String dateFormat = getIntent().getStringExtra("date");
        String sadasd = dateFormat.replace("-", ":");
        text.setText("Person captured: " + sadasd);
    }
}
