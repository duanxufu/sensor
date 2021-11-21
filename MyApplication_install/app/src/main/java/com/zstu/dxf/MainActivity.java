package com.zstu.dxf;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity implements View.OnClickListener {
    private Button mysql;
    private Context context;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        context=MainActivity.this;
        setContentView(R.layout.activity_main);
        mysql=findViewById(R.id.btn_mysql);
        mysql.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.btn_mysql:
                Intent intent = new Intent(context, SqlActivity.class);
                startActivity(intent);startActivity(intent);
        }
    }
}