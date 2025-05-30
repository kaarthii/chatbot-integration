package com.example.ChatBot.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.ChatBot.dto.ChatRequest;
import com.example.ChatBot.service.ChatService;

@RestController
@CrossOrigin(origins="*", allowedHeaders="*")
@RequestMapping("/chat")

public class ChatController {
	@Autowired
	private ChatService chatService;
	
	@PostMapping("/ask")
	public ResponseEntity<Map<String,String>> ask(@RequestBody ChatRequest request) {
		String answer=chatService.handleChat(request);
		Map<String,String>response=new HashMap<>();
		response.put("answer", answer);
		return ResponseEntity.ok().contentType(MediaType.APPLICATION_JSON).body(response);
	}

}
