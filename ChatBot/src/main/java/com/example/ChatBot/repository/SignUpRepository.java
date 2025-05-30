package com.example.ChatBot.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.ChatBot.model.SignUp;

public interface SignUpRepository extends JpaRepository<SignUp,Long> {
	SignUp findByUserName(String userName);

}
