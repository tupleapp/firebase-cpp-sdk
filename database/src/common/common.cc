// Copyright 2016 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "database/src/include/firebase/database/common.h"

#include "app/src/include/firebase/internal/common.h"
#include "database/src/common/query_spec.h"

namespace firebase {
namespace database {

static const char* g_error_messages[] = {
    // kErrorNone
    "The operation was a success, no error occurred.",
    // kErrorDisconnected
    "The operation had to be aborted due to a network disconnect.",
    // kErrorExpiredToken
    "The supplied auth token has expired.",
    // kErrorInvalidToken
    "The specified authentication token is invalid.",
    // kErrorMaxRetries
    "The transaction had too many retries.",
    // kErrorNetworkError
    "The operation could not be performed due to a network error.",
    // kErrorOperationFailed
    "The server indicated that this operation failed.",
    // kErrorOverriddenBySet
    "The transaction was overridden by a subsequent set.",
    // kErrorPermissionDenied
    "This client does not have permission to perform this operation.",
    // kErrorUnavailable
    "The service is unavailable.",
    // kErrorUnknownError
    "An unknown error occurred.",
    // kErrorWriteCanceled
    "The write was canceled locally.",
    // kErrorInvalidVariantType
    "You specified an invalid Variant type for a field.",
    // kErrorConflictingOperationInProgress
    "An operation that conflicts with this one is already in progress.",
    // kErrorTransactionAbortedByUser
    "The transaction was aborted by the user's code.",
};

const char* GetErrorMessage(Error error) {
  return error < FIREBASE_ARRAYSIZE(g_error_messages) ? g_error_messages[error]
                                                      : "";
}

static const Variant* g_server_value_timestamp = nullptr;
const Variant& ServerTimestamp() {
  if (g_server_value_timestamp == nullptr) {
    // The Firebase server defines a ServerValue for Timestamp as a map with the
    // key ".sv" and the value "timestamp".
    std::map<Variant, Variant> server_value;
    server_value.insert(std::make_pair(".sv", "timestamp"));
    g_server_value_timestamp = new Variant(server_value);
  }
  return *g_server_value_timestamp;
}

namespace internal {

std::ostream& operator<<(std::ostream& out, const QuerySpec& query_spec) {
  out << "QuerySpec{";
  out << "path=";
  out << query_spec.path;
  out << ",params=";
  out << query_spec.params;
  out << "}";
  return out;
}

std::ostream& operator<<(std::ostream& out, const QueryParams& query_params) {
  out << "QueryParams{";
  bool needsComma = false;
  if (query_params.order_by) {
    out << "order_by=";
    out << static_cast<int>(query_params.order_by);
    needsComma = true;
  }
  if (!query_params.order_by_child.empty()) {
    if (needsComma) out << ",";
    out << "order_by_child=";
    out << query_params.order_by_child;
    needsComma = true;
  }
  if (query_params.start_at_value.has_value()) {
    if (needsComma) out << ",";
    out << "start_at_value=";
    out << *query_params.start_at_value;
    needsComma = true;
  }
  if (query_params.start_at_child_key.has_value()) {
    if (needsComma) out << ",";
    out << "start_at_child_key=";
    out << *query_params.start_at_child_key;
    needsComma = true;
  }
  if (query_params.end_at_value.has_value()) {
    if (needsComma) out << ",";
    out << "end_at_value=";
    out << *query_params.end_at_value;
    needsComma = true;
  }
  if (query_params.end_at_child_key.has_value()) {
    if (needsComma) out << ",";
    out << "end_at_child_key=";
    out << *query_params.end_at_child_key;
    needsComma = true;
  }
  if (query_params.equal_to_value.has_value()) {
    if (needsComma) out << ",";
    out << "equal_to_value=";
    out << *query_params.equal_to_value;
    needsComma = true;
  }
  if (query_params.equal_to_child_key.has_value()) {
    if (needsComma) out << ",";
    out << "equal_to_child_key=";
    out << *query_params.equal_to_child_key;
    needsComma = true;
  }
  if (query_params.limit_first) {
    if (needsComma) out << ",";
    out << "limit_first=";
    out << query_params.limit_first;
    needsComma = true;
  }
  if (query_params.limit_last) {
    if (needsComma) out << ",";
    out << "limit_last=";
    out << query_params.limit_last;
    needsComma = true;
  }
  out << "}";
  return out;
}

}  // namespace internal
}  // namespace database
}  // namespace firebase
