package com.example.ChatBot.service;

import java.util.List;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.example.ChatBot.dto.ChatRequest;
import com.example.ChatBot.model.ChatHistory;
import com.example.ChatBot.model.ChatSession;
import com.example.ChatBot.repository.ChatHistoryRepository;
import com.example.ChatBot.repository.ChatSessionRepository;

import jakarta.transaction.Transactional;

@Service
public class ChatService {
	@Autowired
    private ChatHistoryRepository historyRepository;
	
	@Autowired
	private ChatSessionRepository sessionRepository;

    private final RestTemplate restTemplate = new RestTemplate();
    @Transactional	
	public String handleChat(ChatRequest chatReq) {
    	ChatSession session = sessionRepository.findById(chatReq.session_id)
    	        .orElseThrow(() -> new RuntimeException("Session not found"));

    	    List<ChatHistory> pastChats = historyRepository.findBySessionId(chatReq.session_id);
		
		StringBuilder contextBuilder = new StringBuilder();
		
		for(ChatHistory chat:pastChats) {
			contextBuilder.append("User: ").append(chat.getQuestion()).append("\n Assistant: ").append(chat.getAnswer()).append("\n");
			
		}
		try {
			JSONObject requestJson=new JSONObject();
			requestJson.put("question", chatReq.question);
			requestJson.put("context", contextBuilder.toString());
			
			HttpHeaders headers = new HttpHeaders();
			headers.setContentType(MediaType.APPLICATION_JSON);
			System.out.println("Going to ask flask");
			HttpEntity<String> entity = new HttpEntity<>(requestJson.toString(), headers);
			String response = restTemplate.postForObject("http://localhost:5000/ask", entity, String.class);
			JSONObject responseJson=new JSONObject(response);
			System.out.println("Flask Response: "+response);
			String answer=responseJson.getString("answer");
			System.out.println("After response");
			
			
			ChatHistory chatHistory=new ChatHistory();
			chatHistory.setUserId(chatReq.user_id);
			chatHistory.setSessionId(chatReq.session_id);
			chatHistory.setQuestion(chatReq.question);
			chatHistory.setAnswer(answer);
			historyRepository.save(chatHistory);
			
			return answer;
		} catch (Exception e) {
			return "Sorry, there was an issue processing your question. please try again";
		}
		
	}

}
