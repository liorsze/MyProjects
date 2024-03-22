package api

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	mockdb "simplebank/db/mock"
	db "simplebank/db/sqlc"
	"simplebank/db/util"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/require"
)

func TestTransferAPI(t *testing.T)  {
	amount := int64(10)

	account1 := randomAccount()
	account2 := randomAccount()
	account3 := randomAccount()

	account1.Currency = util.USD
	account2.Currency = util.USD
	account3.Currency = util.EUR

	testCase := []struct{
		name			string
		Body			gin.H
		buildStubs		func(store *mockdb.MockStore)
		checkResponse	func(recorder *httptest.ResponseRecorder)
	}{
		{
			name: "OK",
			Body: gin.H{
				"from_account_id": account1.ID,
				"to_account_id": account2.ID,
				"amount": amount,
				"currency": util.USD,
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account1.ID)).Times(1).Return(account1,nil)
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account2.ID)).Times(1).Return(account2,nil)

				arg := db.TransferTxParams {
					FromAccountID: account1.ID,
					ToAccountID: account2.ID,
					Amount: amount,
				}

				store.EXPECT().TransferTx(gomock.All(),gomock.Eq(arg)).Times(1)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK,recorder.Code)
			},
		},
		{
			name: "FromAccountNotFound",
			Body: gin.H{
				"from_account_id": account1.ID,
				"to_account_id": account2.ID,
				"amount": amount,
				"currency": util.USD,
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account1.ID)).Times(1).Return(db.Account{},sql.ErrNoRows)
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account2.ID)).Times(0)
				store.EXPECT().TransferTx(gomock.All(),gomock.Any()).Times(0)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusNotFound,recorder.Code)
			},
		},
		{
			name: "ToAccountNotFound",
			Body: gin.H{
				"from_account_id": account1.ID,
				"to_account_id": account2.ID,
				"amount": amount,
				"currency": util.USD,
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account1.ID)).Times(1).Return(account1,nil)
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account2.ID)).Times(1).Return(db.Account{},sql.ErrNoRows)
				store.EXPECT().TransferTx(gomock.All(),gomock.Any()).Times(0)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusNotFound,recorder.Code)
			},
		},
		{
			name: "FromAccountCurrencyMissmatch",
			Body: gin.H{
				"from_account_id": account3.ID,
				"to_account_id": account2.ID,
				"amount": amount,
				"currency": util.USD,
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account3.ID)).Times(1).Return(account3,nil)
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account2.ID)).Times(0)
				store.EXPECT().TransferTx(gomock.All(),gomock.Any()).Times(0)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusBadRequest,recorder.Code)
			},
		},
		{
			name: "ToAccountCurrencyMissmatch",
			Body: gin.H{
				"from_account_id": account1.ID,
				"to_account_id": account3.ID,
				"amount": amount,
				"currency": util.USD,
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account1.ID)).Times(1).Return(account1,nil)
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account3.ID)).Times(1).Return(account3,nil)
				store.EXPECT().TransferTx(gomock.All(),gomock.Any()).Times(0)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusBadRequest,recorder.Code)
			},
		},
		{
			name: "InvalidCurrency",
			Body: gin.H{
				"from_account_id": account1.ID,
				"to_account_id": account2.ID,
				"amount": amount,
				"currency": "invalid",
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Any()).Times(0)
				store.EXPECT().TransferTx(gomock.All(),gomock.Any()).Times(0)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusBadRequest,recorder.Code)
			},
		},
		{
			name: "NegativeAmount",
			Body: gin.H{
				"from_account_id": account1.ID,
				"to_account_id": account2.ID,
				"amount": -amount,
				"currency": util.USD,
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Any()).Times(0)
				store.EXPECT().TransferTx(gomock.All(),gomock.Any()).Times(0)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusBadRequest,recorder.Code)
			},
		},
		{
			name: "GetAccountError",
			Body: gin.H{
				"from_account_id": account1.ID,
				"to_account_id": account2.ID,
				"amount": amount,
				"currency": util.USD,
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Any()).Times(1).Return(db.Account{},sql.ErrConnDone)
				store.EXPECT().TransferTx(gomock.All(),gomock.Any()).Times(0)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusInternalServerError,recorder.Code)
			},
		},
		{
			name: "TransferTxError",
			Body: gin.H{
				"from_account_id": account1.ID,
				"to_account_id": account2.ID,
				"amount": amount,
				"currency": util.USD,
			},
			buildStubs: func(store *mockdb.MockStore) {
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account1.ID)).Times(1).Return(account1,nil)
				store.EXPECT().GetAccount(gomock.Any(),gomock.Eq(account2.ID)).Times(1).Return(account2,nil)
				store.EXPECT().TransferTx(gomock.All(),gomock.Any()).Times(1).Return(db.TransferTxResult{},sql.ErrConnDone)

			},
			checkResponse: func(recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusInternalServerError,recorder.Code)
			},
		},
	}

	for i := range testCase {
		tc := testCase[i]

		t.Run(tc.name, func(t *testing.T) {
			ctrl := gomock.NewController(t)
			defer ctrl.Finish()

			store := mockdb.NewMockStore(ctrl)
			tc.buildStubs(store)

			server := NewServer(store)
			recorder := httptest.NewRecorder()

			data, err := json.Marshal(tc.Body)
			require.NoError(t,err)

			url := "/transfers"
			request, err := http.NewRequest(http.MethodPost,url,bytes.NewReader(data))
			require.NoError(t,err)

			server.router.ServeHTTP(recorder,request)
			tc.checkResponse(recorder)
		})
	}

}