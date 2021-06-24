package com.example.catchingcomputersapp;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.ListResult;
import com.google.firebase.storage.StorageReference;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class picturesActivity  extends AppCompatActivity {
    private RecyclerView recyclerView;
    private String busID;
    private MyAdapter myAdapter;
    private Context ctx;
    private List<ImgDataUrl> imgDataUrls;
    public List<String> imgTimeStamps;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_faces);
        imgDataUrls = new ArrayList<ImgDataUrl>();
        imgTimeStamps = new ArrayList<>();
        recyclerView=(RecyclerView)findViewById(R.id.recyclerView);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        myAdapter = new MyAdapter(imgDataUrls, imgTimeStamps, this);
        recyclerView.setAdapter(myAdapter);
        Intent i = getIntent();
        busID = i.getStringExtra("busID");
        ctx = this;
        getData();

        findViewById(R.id.refreshButton).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                imgDataUrls.clear();
                imgTimeStamps.clear();
                myAdapter = new MyAdapter(imgDataUrls, imgTimeStamps, ctx);
                recyclerView.setAdapter(myAdapter);
                getData();
            }
        });

    }
    private void getData() {
        if (imgDataUrls == null){
            imgDataUrls = new ArrayList<ImgDataUrl>();
        }
        if (imgTimeStamps == null){
            imgTimeStamps = new ArrayList<String>();
        }
        FirebaseStorage storage = FirebaseStorage.getInstance();
        StorageReference bla = storage.getReference().child(busID + "/entranceCam");
        bla.listAll().addOnSuccessListener(new OnSuccessListener<ListResult>() {
            @Override
            public void onSuccess(ListResult listResult) {
                for (StorageReference item: listResult.getItems()){
                    item.getDownloadUrl().addOnSuccessListener(new OnSuccessListener<Uri>() {
                        @Override
                        public void onSuccess(Uri uri) {
                            if (!uri.getPath().contains(".jpg")){
                                return;
                            }
                            Pattern pattern = Pattern.compile(".*T([\\d*-]*)");
                            Matcher matcher = pattern.matcher(uri.toString());
                            matcher.find();
                            String group = matcher.group(1);
                            imgTimeStamps.add(group);
                            imgDataUrls.add(new ImgDataUrl(uri.toString()));
                            myAdapter.notifyItemInserted(imgDataUrls.size() - 1);
                        }
                    });
                }
            }
        });
    }
}

class ImgDataUrl {
    public String imageUrl;

    public ImgDataUrl(){

    }

    public ImgDataUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
}

class MyAdapter extends RecyclerView.Adapter<MyAdapter.ViewHolder> {
    List<ImgDataUrl> imgDataUrls;
    List<String> imgTimeStamps;
    Context context;

    public MyAdapter(List<ImgDataUrl> imgDataUrls,List<String> imageTimeStamps, Context context) {
        this.imgTimeStamps = imageTimeStamps;
        this.imgDataUrls = imgDataUrls;
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view= LayoutInflater.from(parent.getContext()).inflate(R.layout.activity_faces_item,parent,false);
        return new ViewHolder(view);
    }


    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        ImgDataUrl imgDataUrl = imgDataUrls.get(position);
        Glide.with(context)
                .load(imgDataUrl.getImageUrl())
                .into(holder.imageView);
        holder.dataCreated = imgTimeStamps.get(position);
    }

    @Override
    public int getItemCount() {
        return imgDataUrls.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder{
        private ImageView imageView;
        private String dataCreated;
        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            imageView=(ImageView)itemView.findViewById(R.id.image_view);
            imageView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Intent _intent = new Intent(context, imageDataActivity.class);
                    Bitmap _bitmap = ((BitmapDrawable) imageView.getDrawable()).getBitmap();
                    ByteArrayOutputStream _bs = new ByteArrayOutputStream();
                    _bitmap.compress(Bitmap.CompressFormat.JPEG, 50, _bs);
                    _intent.putExtra("byteArray", _bs.toByteArray());
                    _intent.putExtra("date", dataCreated);
                    context.startActivity(_intent);
                    // TODO: OPEN ACTIVITY WITH IMAGE + METADATA
                }
            });
        }
    }
}